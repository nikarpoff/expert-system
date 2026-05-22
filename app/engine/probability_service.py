from app.utils.math_utils import safe_divide


def bayes_update(current_p: float, p_x_w: float, p_x_not_w: float, answer_yes: bool) -> float:
    if answer_yes:
        numerator = current_p * p_x_w
        denominator = numerator + (1 - current_p) * p_x_not_w
    else:
        numerator = current_p * (1 - p_x_w)
        denominator = numerator + (1 - current_p) * (1 - p_x_not_w)
    return safe_divide(numerator, denominator, default=current_p)
