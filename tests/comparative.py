import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MODES = ("traditional", "generative")
CATEGORIES = ("ACCESS", "BUG", "FEATURE", "SECURITY")
PRIORITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")
RESPONSE_FIELDS = {"category", "priority", "response", "requiresHumanReview", "mode"}


def analyze(endpoint, message, mode, timeout):
    payload = json.dumps({"message": message, "mode": mode}, ensure_ascii=False)
    request = Request(
        endpoint,
        data=payload.encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as reply:
            status = reply.status
            body = reply.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        with error:
            status = error.code
            body = error.read().decode("utf-8", errors="replace")
    except (URLError, OSError) as error:
        return {"status": None, "body": None, "error": str(error)}

    return {"status": status, "body": body}


def evaluate(reply, mode, case):
    try:
        data = json.loads(reply["body"] or "null")
    except json.JSONDecodeError:
        data = None
    if not isinstance(data, dict):
        data = {}

    category = data.get("category")
    priority = data.get("priority")
    response = data.get("response")
    human_review = data.get("requiresHumanReview")
    valid_format = (
        reply["status"] == 200
        and data.keys() == RESPONSE_FIELDS
        and category in CATEGORIES
        and priority in PRIORITIES
        and isinstance(response, str)
        and bool(response.strip())
        and isinstance(human_review, bool)
        and data.get("mode") == mode
    )
    correct_classification = valid_format and (category, priority) == (
        case["category"], case["priority"]
    )
    return {
        "mode": mode,
        **reply,
        "category": category,
        "priority": priority,
        "requiresHumanReview": human_review,
        "valid_format": valid_format,
        "correct_classification": correct_classification,
    }


def flag(value):
    return "Sí" if value else "No"


def markdown_cell(value):
    if value is None:
        return "—"
    return str(value).replace("|", r"\|").replace("\n", " ")


def report_markdown(results, summaries):
    lines = [
        "# Resultados comparativos",
        "",
        "Una clasificación cuenta como correcta si la API cumple el contrato y coincide con la categoría y la prioridad de referencia. El porcentaje usa todos los casos, incluidos los errores de ejecución.",
        "",
        "| Caso | Tipo | Motor | Referencia | Categoría | Prioridad | Formato válido | Clasificación correcta | Revisión humana | HTTP |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in results:
        case = item["reference"]
        for run in item["runs"]:
            review = run["requiresHumanReview"]
            cells = (
                case["id"], case["type"], run["mode"],
                f'{case["category"]} / {case["priority"]}',
                run["category"], run["priority"], flag(run["valid_format"]),
                flag(run["correct_classification"]),
                flag(review) if isinstance(review, bool) else None,
                run["status"],
            )
            lines.append("| " + " | ".join(map(markdown_cell, cells)) + " |")

    lines.extend([
        "",
        "| Motor | Formato válido | Resultados correctos | Porcentaje correcto |",
        "| --- | --- | --- | --- |",
    ])
    for mode, summary in summaries.items():
        lines.append(
            f'| `{mode}` | {summary["valid_format"]}/{summary["total"]} | '
            f'{summary["correct"]}/{summary["total"]} | {summary["accuracy"]:.2f}% |'
        )

    lines.extend(["", "Las solicitudes y las respuestas HTTP completas están en [results.json](results.json).", ""])
    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Compara ambos motores mediante la API.")
    parser.add_argument("--endpoint", default="http://localhost:8000/api/analyze")
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout debe ser mayor que cero")

    cases = json.loads((root / "tests" / "comparative_cases.json").read_text(encoding="utf-8"))
    results = []
    by_mode = {mode: [] for mode in MODES}
    for case in cases:
        runs = []
        for mode in MODES:
            reply = analyze(args.endpoint, case["message"], mode, args.timeout)
            outcome = evaluate(reply, mode, case)
            runs.append(outcome)
            by_mode[mode].append(outcome)
            print(f'{case["id"]} {mode}: HTTP {reply["status"]}', flush=True)
        results.append({"reference": case, "runs": runs})

    summaries = {}
    for mode, runs in by_mode.items():
        correct = sum(run["correct_classification"] for run in runs)
        summaries[mode] = {
            "total": len(runs),
            "valid_format": sum(run["valid_format"] for run in runs),
            "correct": correct,
            "accuracy": round(100 * correct / len(runs), 2),
        }

    evidence = root / "evidence"
    evidence.mkdir(exist_ok=True)
    report = {"summaries": summaries, "results": results}
    (evidence / "results.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (evidence / "RESULTADOS.md").write_text(report_markdown(results, summaries), encoding="utf-8")

    return int(any(run["status"] != 200 for runs in by_mode.values() for run in runs))


if __name__ == "__main__":
    raise SystemExit(main())
