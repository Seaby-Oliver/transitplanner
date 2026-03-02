import pandas as pd

def check_observability_table(planet_list, export_csv=None, export_excel=None):
    """
    Generate a summary table of observability results.

    This function collects key parameters and observability decisions into
    a structured table suitable for printing or exporting to file formats.

    Optional CSV and Excel outputs allow results to be saved for later analysis.

    Parameters
    planet_list
    List of enriched planet dictionaries including observability status

    export_csv
    Optional path to export CSV file

    export_excel
    Optional path to export Excel file

    Returns
    Pandas DataFrame containing the observability summary
    """

    summary_data = []

    for planet in planet_list:
        summary_data.append({
            "Planet": planet['Object'],
            "Transit Start (UTC)": planet['Transit Start (UTC)'],
            "Mid-Transit (UTC)": planet['Mid-Transit (UTC)'],
            "Transit End (UTC)": planet['Transit End (UTC)'],
            "Rp/Rs": planet.get('RpRs'),
            "a/Rs": planet.get('aRs'),
            "Inclination (deg)": planet.get('inclination'),
            "Transit depth (mmag)": planet.get('Transit Depth (mmag)'),
            "Duration (min)": planet['Duration (hours)']*60,
            "R mag": planet.get('R Magnitude'),
            "SNR": planet.get('SNR'),
            "RA": planet['RA'],
            "DEC": planet['Dec'],
            "Status": planet['Status'],
             "Priority": planet.get("priority")
        })

    df = pd.DataFrame(summary_data)
    if export_csv:
        df.to_csv(export_csv, index=False)
    if export_excel:
        df.to_excel(export_excel, index=False)
    return df






