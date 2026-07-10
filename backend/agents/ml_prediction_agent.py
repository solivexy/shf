import time
import logging
import pandas as pd
from models.state import HedgeFundState
from models.schemas import MLPredictionOutput
from agents.base_agent import emit_timeline_log
from utils.cache import cache_manager
from ml.prediction_engine import ml_prediction_engine

logger = logging.getLogger("ml_prediction_agent")


async def ml_prediction_agent_node(state: HedgeFundState) -> HedgeFundState:
    """
    Independent Machine Learning Prediction Agent.
    Evaluates XGBoost, LightGBM, and Random Forest models on historical technical and macro features.
    Provides return probability and direction (UP, DOWN, SIDEWAYS) without making direct Buy/Sell decisions.
    """
    ticker = state.get("ticker", "AAPL").upper()
    start_time = time.time()
    emit_timeline_log(state, "ML Prediction Agent", "RUNNING")
    logger.info(f"ML Prediction Agent running for ticker: {ticker}")

    # Load asset OHLCV
    raw_dict = await cache_manager.get(f"df_ohlcv:{ticker}")
    df = pd.DataFrame(raw_dict) if raw_dict else None

    macro_data = state.get("macro_economy")
    macro_score = macro_data.macro_score if macro_data else 0.0

    prediction_dict = ml_prediction_engine.train_and_predict(df, macro_score=macro_score)

    output = MLPredictionOutput(
        ticker=ticker,
        probability_up=float(prediction_dict["probability_up"]),
        expected_return_percent=float(prediction_dict["expected_return_percent"]),
        predicted_direction=str(prediction_dict["predicted_direction"]),
        feature_importance=prediction_dict["feature_importance"],
        model_used=str(prediction_dict["model_used"])
    )

    state["ml_prediction"] = output
    emit_timeline_log(
        state,
        "ML Prediction Agent",
        "COMPLETED",
        runtime_ms=(time.time() - start_time) * 1000,
        confidence=round(output.probability_up * 100.0, 1),
        summary=f"Ensemble Probability: {round(output.probability_up * 100, 1)}% ({output.predicted_direction}). Expected Horizon Return: {output.expected_return_percent:+g}%.",
        output_json=output
    )
    return state
