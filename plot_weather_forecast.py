from datetime import datetime, timezone
from pathlib import Path
import re
from urllib.parse import quote

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import requests


# Set your API key from the Global Weather Data User Center.
API_KEY = "PASTE_YOUR_API_KEY_HERE"
LOCATION = "5368361"  # Los Angeles GeoNameID; use an ID to avoid URL-encoding ambiguity.
OUTPUT_DIR = Path(__file__).parent
API_BASE_URL = "https://global-weather-data.com/api/forecast"


def fetch_forecast():
    if not API_KEY or API_KEY == "PASTE_YOUR_API_KEY_HERE":
        raise ValueError("Set API_KEY at the top of this script before running it.")

    url = f"{API_BASE_URL}/{quote(LOCATION, safe=',')}/{API_KEY}"
    requested_at = datetime.now(timezone.utc)
    response = requests.get(url, timeout=60)
    if not response.ok:
        raise RuntimeError(
            f"Forecast request failed with HTTP {response.status_code}. "
            "Check the API key, location, and request limit."
        )
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(f"Forecast API returned an error: {payload.get('message', payload)}")
    return payload, requested_at


def parse_utc_time(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def plot_forecast(payload, requested_at):
    location = payload["location_info"]
    location_slug = re.sub(r"[^A-Za-z0-9]+", "_", location["name"]).strip("_")
    output_png = OUTPUT_DIR / f"{location_slug}_15_day_forecast.png"
    output_pdf = OUTPUT_DIR / f"{location_slug}_15_day_forecast.pdf"
    forecast = payload["forecast_data"]
    times = [parse_utc_time(value) for value in forecast["time"]]
    if not times:
        raise ValueError("The forecast API returned no time values.")
    if any(len(values) != len(times) for values in forecast.values()):
        raise ValueError("Forecast variables do not all match the time dimension.")

    def values(key):
        return np.array(
            [np.nan if value is None else float(value) for value in forecast[key]],
            dtype=float,
        )

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 10,
        "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.1,
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "axes.edgecolor": "#b8c2cc",
        "axes.linewidth": 0.7,
        "grid.color": "#dbe2e8",
        "grid.linewidth": 0.55,
        "grid.alpha": 0.75,
        "savefig.facecolor": "#ffffff",
        "savefig.bbox": "tight",
    })

    colors = {
        "navy": "#17324d", "blue": "#2878b5", "teal": "#168c8c",
        "orange": "#e07a2d", "coral": "#cf5c5c", "purple": "#8064a2",
        "gold": "#c49a28", "dark": "#34495e", "cyan": "#43a6b8",
    }
    fig, axes = plt.subplots(
        8, 1, figsize=(16, 20.5), sharex=True,
        gridspec_kw={"height_ratios": [1.05, 1.2, .82, 1, .72, 1.25, .78, .8]},
    )
    fig.subplots_adjust(left=.075, right=.985, top=.932, bottom=.065, hspace=.24)
    fig.text(
        .075, .975,
        f"{location['name'].upper()} | 15-DAY HOURLY CITY FORECAST",
        color=colors["navy"], fontsize=16, fontweight="bold", ha="left", va="top",
    )
    fig.text(
        .075, .953,
        f"{location.get('admin1', '')}, {location.get('country', '')} | "
        f"{len(times)} hourly records | ALL TIMES UTC | "
        f"{times[0]:%d %b %Y %H:%M} - {times[-1]:%d %b %Y %H:%M} UTC",
        color="#536273", fontsize=9, ha="left", va="top",
    )
    for ax in axes:
        ax.grid(True, axis="y")
        ax.grid(True, axis="x", alpha=.38)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#c7d0d9")
        ax.spines["bottom"].set_color("#c7d0d9")
        ax.tick_params(length=2.5, color="#8c99a6")
        ax.axvline(requested_at, color="#596a7b", lw=1, ls=(0, (4, 3)), zorder=5)

    plotted = set()
    ax = axes[0]
    for key, label, color, style in [
        ("t2m", "2 m air temperature | t2m", colors["navy"], "-"),
        ("d2m", "2 m dew point | d2m", colors["teal"], "-"),
        ("skt", "Skin temperature | skt", colors["orange"], "--"),
    ]:
        ax.plot(times, values(key), color=color, lw=1.4, ls=style, label=label)
        plotted.add(key)
    ax.set_ylabel("deg C")
    ax.set_title("01  Temperature", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=3, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[1]
    for key, label, color, style in [
        ("u10", "10 m eastward | u10", colors["blue"], "-"),
        ("v10", "10 m northward | v10", colors["teal"], "-"),
        ("u100", "100 m eastward | u100", colors["orange"], "--"),
        ("v100", "100 m northward | v100", colors["purple"], "--"),
        ("fg10", "10 m gust | fg10", colors["coral"], ":"),
    ]:
        ax.plot(times, values(key), color=color, lw=1.15, ls=style, label=label)
        plotted.add(key)
    ax.axhline(0, color="#8995a1", lw=.65)
    ax.set_ylabel("m/s")
    ax.set_title("02  Wind components and gust", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=3, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[2]
    for key, label, color, style in [
        ("msl", "Mean sea-level pressure | msl", colors["navy"], "-"),
        ("sp", "Surface pressure | sp", colors["gold"], "--"),
    ]:
        ax.plot(times, values(key), color=color, lw=1.35, ls=style, label=label)
        plotted.add(key)
    ax.set_ylabel("hPa")
    ax.set_title("03  Atmospheric pressure", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=2, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[3]
    x = mdates.date2num(times)
    bar_width = (1 / 24) * .22
    for key, label, color, offset in [
        ("tp", "Total precipitation | tp", colors["blue"], -bar_width),
        ("sf", "Snowfall | sf", colors["cyan"], 0),
        ("ro", "Runoff | ro", colors["orange"], bar_width),
    ]:
        ax.bar(
            x + offset, values(key), width=bar_width, color=color,
            alpha=.72, linewidth=0, label=label, zorder=3,
        )
        plotted.add(key)
    ax.plot(times, values("sd"), color=colors["dark"], lw=1.05, ls="--", label="Snow depth | sd", zorder=4)
    plotted.add("sd")
    ax.set_ylabel("mm")
    ax.set_title("04  Precipitation, snow and runoff", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=4, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[4]
    cloud = values("tcc")
    ax.fill_between(times, 0, cloud, color=colors["cyan"], alpha=.17, linewidth=0)
    ax.plot(times, cloud, color=colors["teal"], lw=1.3, label="Total cloud cover | tcc")
    plotted.add("tcc")
    ax.set_ylim(-.04, 1.06)
    ax.set_ylabel("fraction")
    ax.set_title("05  Cloud cover", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[5]
    for key, label, color, style in [
        ("ssrd", "Surface solar downward | ssrd", colors["gold"], "-"),
        ("strd", "Surface thermal downward | strd", colors["purple"], "-"),
        ("ssr", "Surface net solar | ssr", colors["blue"], "--"),
        ("str", "Surface net thermal | str", colors["teal"], "--"),
        ("ttr", "Top net thermal | ttr", colors["coral"], ":"),
    ]:
        ax.plot(times, values(key), color=color, lw=1.05, ls=style, label=label)
        plotted.add(key)
    ax.axhline(0, color="#8995a1", lw=.65)
    ax.set_ylabel("W/m2")
    ax.set_title("06  Radiation fluxes", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=3, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[6]
    cape = values("mucape")
    ax.fill_between(times, 0, cape, color=colors["orange"], alpha=.14, linewidth=0)
    ax.plot(times, cape, color=colors["orange"], lw=1.25, label="Most-unstable CAPE | mucape")
    plotted.add("mucape")
    ax.set_ylabel("J/kg")
    ax.set_title("07  Convective instability", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    ax = axes[7]
    for key, label, color, style in [
        ("tcw", "Total column water | tcw", colors["blue"], "-"),
        ("tcwv", "Total column water vapor | tcwv", colors["teal"], "--"),
    ]:
        ax.plot(times, values(key), color=color, lw=1.3, ls=style, label=label)
        plotted.add(key)
    ax.set_ylabel("kg/m2")
    ax.set_title("08  Column water", loc="left", color=colors["navy"], fontweight="bold", pad=5)
    ax.legend(loc="upper left", ncol=2, frameon=True, framealpha=.92, edgecolor="#dbe2e8")

    expected = set(forecast) - {"time"}
    if plotted != expected:
        raise ValueError(f"Chart does not cover all returned variables: {expected - plotted}")
    locator = mdates.AutoDateLocator(minticks=7, maxticks=10, tz=timezone.utc)
    axes[-1].xaxis.set_major_locator(locator)
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%d %b", tz=timezone.utc))
    axes[-1].set_xlim(times[0], times[-1])
    axes[-1].set_xlabel("Forecast validity | UTC", labelpad=7)
    for ax in axes[:-1]:
        ax.tick_params(labelbottom=False)
    fig.text(
        .985, .012,
        f"Dashed line: API request time ({requested_at:%d %b %Y %H:%M} UTC). "
        "All 23 meteorological variables are shown; time is the shared UTC x-axis.",
        ha="right", va="bottom", fontsize=7.3, color="#637282",
    )
    fig.savefig(output_png, dpi=240)
    fig.savefig(output_pdf)
    plt.close(fig)
    return len(times), len(plotted), output_png, output_pdf


def main():
    payload, requested_at = fetch_forecast()
    records, variables, output_png, output_pdf = plot_forecast(payload, requested_at)
    print(
        f"Saved {output_png} and {output_pdf}; "
        f"{records} hourly records, {variables} meteorological variables, all times UTC."
    )


if __name__ == "__main__":
    main()
