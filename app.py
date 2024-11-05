import plotly.express as px
import seaborn as sb
import palmerpenguins as pp
from shiny.express import input, render, ui
from shinywidgets import render_plotly
from shiny import render
import plotly.graph_objects as go

p_df = pp.load_penguins()

ui.page_opts(title="Filling layout", fillable=True)

with ui.sidebar(bg="#808080"):
    ui.h1("This is my sidebar - there are many like it but this one is mine")
    ui.hr()
    ui.a("Github", href="https://github.com/JSellinger", target="_blank")

    ui.h2("Selection Settings")
    with ui.card():
        ui.card_header("Settings")
        ui.input_dark_mode()
        ui.hr()
    with ui.card():
        ui.hr()
        ui.card_header("Stupid Fricking Inputs")
        ui.input_slider("n", "Slider for Bin ", 0, 100, 10)
        ui.input_selectize(
            "s", "Select Island for Scatterplot", ["Dream", "Biscoe", "Torgersen"]
        )
        ui.input_numeric("num", "Background Color", 0)
        ui.input_checkbox_group(
            "check", "Species for Data Grid/Table", ["Adelie", "Gentoo", "Chinstrap"]
        )

with ui.layout_columns():

    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        def table1():
            selected_species = input.check()  # Get selected species from the checkbox
            # Filter the DataFrame based on the selected species
            if selected_species:
                filtered_df = p_df[p_df["species"].isin(selected_species)]
            else:
                filtered_df = (
                    p_df  # Return the full DataFrame if no species are selected
                )
            return render.DataTable(filtered_df)  # Return the filtered DataFrame

    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        def datagrid1():
            selected_species = input.check()  # Get selected species from the checkbox
            # Filter the DataFrame based on the selected species
            if selected_species:
                filtered_df = p_df[p_df["species"].isin(selected_species)]
            else:
                filtered_df = (
                    p_df  # Return the full DataFrame if no species are selected
                )
            return render.DataGrid(filtered_df)  # Return the filtered DataFrame


with ui.layout_columns():

    with ui.card():
        ui.card_header("Plotly Histogram - Species")

        @render_plotly
        def plot1():
            num_n = input.n()
            return px.histogram(p_df, y="species", nbins=num_n)

    with ui.card():
        ui.card_header("Seaborn Histogram - Species")

        @render.plot
        def plot2():
            return sb.histplot(p_df, y="species", bins=input.n())

    with ui.card():

        @render_plotly
        def plot3():
            s_lands = [input.s()]

            if s_lands:
                filtered_df = p_df[p_df["island"].isin(s_lands)]
            else:
                filtered_df = p_df

            return px.scatter(
                filtered_df, x="body_mass_g", y="flipper_length_mm", color="species"
            )
