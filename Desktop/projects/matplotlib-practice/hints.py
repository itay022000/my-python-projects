"""Strike-1 hint strings for matplotlib-practice (B015)."""

from __future__ import annotations

# H3 hint templates (strike 1 only; conceptual — avoid exact syntax/API names)
HINT_NP_ARRAY = (
    "Build a NumPy array from the values in the step; "
)
HINT_NP_RANDOM_NORMAL = (
    "NumPy can draw random samples from a normal distribution "
    "using mean, spread, and count."
)
HINT_LABELS_ARRAY = (
    "Turn the category labels into a string array, "
    "keeping the same order as above."
)
HINT_HEIGHTS_ARRAY = (
    "Turn the bar heights into a numeric array, "
    "keeping the same order as above."
)
HINT_PLT_HIST = "Matplotlib can draw a histogram from your data array."
HINT_PLT_BAR = (
    "Bar charts pair labels with heights; "
    "check the specs for orientation or styling."
)
HINT_PLT_PIE = (
    "Pie charts need slice sizes, colors, and labels; "
    "see the specs for any extra options."
)
HINT_PLT_LEGEND = (
    "You can add a legend after the chart; "
    "check whether a title is required."
)
HINT_PLT_PLOT = (
    "Line plots need x and y data; "
    "optional styling may be listed in the specs."
)
HINT_PLT_SUBPLOT = (
    "Subplots sit on a row/column grid; "
    "the step tells you which cell to use."
)
HINT_TITLE_LABEL = (
    "Chart titles and axis labels are set in separate calls; "
    "match the text from the step."
)
HINT_SCATTER_PLOT = (
    "Scatter plots map x and y points; "
    "color and point size may be optional."
)
