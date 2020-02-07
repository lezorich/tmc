import decimal
import logging

import requests
from lxml import html

logger = logging.getLogger(__name__)

TMC_SBIF_URL = "https://sbif.cl/sbifweb/servlet/InfoFinanciera"

SBIF_TMC_OPERATION_TYPES = ["adjustable", "non_adjustable"]


class ExternalServiceError(Exception):
    pass


def get_sbif_tmc(
    credit_amount_uf,
    credit_term_days,
    valid_at,
    operation_type="non_adjustable",
):
    tmc_row_idx = _map_credit_to_tmc_row(
        credit_amount_uf, credit_term_days, operation_type
    )
    return _scrape_tmc_from_sbif(tmc_row_idx, valid_at)


def _scrape_tmc_from_sbif(tmc_idx, valid_at):
    tree = html.fromstring(_get_sbif_html(valid_at))
    tmc_table = tree.xpath("//*[@id='contenido']/div[1]/table")[0]
    tmc_rows = tmc_table.findall("tr")
    return decimal.Decimal(_get_tmc_of_row(tmc_rows[tmc_idx]))


def _map_credit_to_tmc_row(credit_amount_uf, credit_term_days, operation_type):
    if operation_type == "non_adjustable":
        return _map_adjustable_credit_to_tmc_row(
            credit_amount_uf, credit_term_days
        )
    return _map_non_adjustable_credit_to_tmc_row(
        credit_amount_uf, credit_term_days
    )


def _map_adjustable_credit_to_tmc_row(credit_amount_uf, credit_term_days):
    if credit_term_days < 90:
        if credit_amount_uf <= 5000:
            return 1
        return 2
    if credit_amount_uf <= 50:
        return 4
    if credit_amount_uf <= 200:
        return 5
    if credit_amount_uf <= 5000:
        return 6
    return 7


def _map_non_adjustable_credit_to_tmc_row(credit_amount_uf, credit_term_days):
    if credit_term_days < 365:
        return 9
    if credit_amount_uf <= 2000:
        return 10
    return 11


def _get_sbif_html(valid_at):
    params = {"indice": "4.2.1", "FECHA": valid_at}
    try:
        req = requests.get(TMC_SBIF_URL, params=params)
    except requests.exceptions.RequestException:
        logger.error(
            "GET request with params %s to %s failed",
            str(params),
            TMC_SBIF_URL,
            exc_info=True,
        )
        raise ExternalServiceError(
            "Failed to access SBIF website. See logs for more details."
        )
    return req.content


def _get_tmc_of_row(row):
    tmc_html = row.findall("td")[-1]
    tmc_text = tmc_html.text
    tmc = tmc_text.split("%")[0]
    return tmc.strip()
