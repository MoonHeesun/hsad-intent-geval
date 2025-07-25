from src.geval import geval
import json
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional


def get_user_inputs() -> Tuple[int, str]:
    """Get number of iterations and save format from user input"""
    # Get iteration count
    while True:
        try:
            n = int(input("Enter the number of evaluation iterations: "))
            if n < 1:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Get save format
    while True:
        print("\nSelect save format:")
        print("1. JSON only")
        print("2. Excel only")
        print("3. Both JSON and Excel")

        try:
            format_choice = int(input("Enter your choice (1-3): "))
            if format_choice == 1:
                save_format = "json"
                break
            elif format_choice == 2:
                save_format = "excel"
                break
            elif format_choice == 3:
                save_format = "both"
                break
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return n, save_format


def save_summary_results(
    all_iterations: List[Dict[str, Any]],
    timestamp: str,
    avg_score: float,
    save_format: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Save summary of all iterations based on selected format"""
    summary_json = None
    summary_excel = None

    # Prepare summary data
    summary_data = {
        "total_iterations": len(all_iterations),
        "overall_average_score": avg_score,
        "iteration_scores": [iter_data["metric_score"] for iter_data in all_iterations],
        "iterations": all_iterations,
    }

    if save_format in ["json", "both"]:
        summary_json = f"results/evaluation_summary_{timestamp}.json"
        with open(summary_json, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)

    if save_format in ["excel", "both"]:
        # Create summary Excel
        summary_df = pd.DataFrame(
            [
                {
                    "iteration": i + 1,
                    "score": iter_data["metric_score"],
                    "samples_evaluated": len(iter_data.get("detailed_results", [])),
                }
                for i, iter_data in enumerate(all_iterations)
            ]
        )
        summary_df.loc[len(summary_df)] = {
            "iteration": "Overall Average",
            "score": avg_score,
            "samples_evaluated": summary_df["samples_evaluated"].sum(),
        }

        summary_excel = f"results/evaluation_summary_{timestamp}.xlsx"
        summary_df.to_excel(summary_excel, index=False)

    return summary_json, summary_excel


if __name__ == "__main__":
    n, save_format = get_user_inputs()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    all_iterations = []
    total_score = 0

    print(f"\n🚀 Starting {n} evaluation iterations...")
    print(f"📁 Save format: {save_format.upper()}")

    for i in range(n):
        print(f"\n📊 Running iteration {i + 1}/{n}...")
        results = geval()

        # Collect iteration data
        iteration_data = {
            "iteration": i + 1,
            "metric_score": results.metric_score,
            "metric_explanation": results.metric_explanation,
            "detailed_results": results.detailed_results,
        }
        all_iterations.append(iteration_data)
        total_score += results.metric_score

        print(f"✅ Iteration {i + 1} completed! Score: {results.metric_score:.3f}")

    # Calculate overall average
    overall_average = total_score / n

    # Save summary results
    summary_json, summary_excel = save_summary_results(
        all_iterations, timestamp, overall_average, save_format
    )

    print(f"\n{'='*50}")
    print(f"🎯 All iterations completed!")
    print(f"{'='*50}")
    print(f"📈 Individual iteration scores:")
    for i, iter_data in enumerate(all_iterations):
        print(f"   Iteration {i + 1}: {iter_data['metric_score']:.3f}")
    print(f"\n🏆 Overall Average Score: {overall_average:.3f}")

    print(f"\n💾 Summary results saved to:")
    if summary_json:
        print(f"   - JSON: {summary_json}")
    if summary_excel:
        print(f"   - Excel: {summary_excel}")
