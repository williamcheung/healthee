from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the HTML files directory
app.mount("/html_files", StaticFiles(directory="./html_files"), name="html_files")

# Return HTML with embedded iframes
@app.get("/", response_class=HTMLResponse)
def read_root():
    dropdown = ''.join([f'<option value="{i}">Cohort {i}</option>' for i in range(1, 11)])
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cohort Visualizations</title>
        <style>
            .dropdown-container {{
                margin-bottom: 10px;  /* Small gap between dropdowns */
            }}
        </style>
    </head>
    <body>
        <h3>Select Cohorts to View Visualizations</h3>

        <div class="dropdown-container">
            <label for="dropdown1">Cohort:</label>
            <select id="dropdown1" onchange="updateIframes(1)">
                <option value="">Select Cohort</option>
                {dropdown}
            </select>
        </div>
        <div id="cohort1_iframes" style="display: none; margin-top: 20px;">
            <div style="display: flex; justify-content: space-between;">
                <iframe id="iframe1_1" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe1_2" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe1_3" width="33%" height="500px" frameborder="0"></iframe>
            </div>
        </div>

        <div class="dropdown-container">
            <label for="dropdown2">Cohort:</label>
            <select id="dropdown2" onchange="updateIframes(2)">
                <option value="">Select Cohort</option>
                {dropdown}
            </select>
        </div>
        <div id="cohort2_iframes" style="display: none; margin-top: 20px;">
            <div style="display: flex; justify-content: space-between;">
                <iframe id="iframe2_1" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe2_2" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe2_3" width="33%" height="500px" frameborder="0"></iframe>
            </div>
        </div>

        <div class="dropdown-container">
            <label for="dropdown3">Cohort:</label>
            <select id="dropdown3" onchange="updateIframes(3)">
                <option value="">Select Cohort</option>
                {dropdown}
            </select>
        </div>
        <div id="cohort3_iframes" style="display: none; margin-top: 20px;">
            <div style="display: flex; justify-content: space-between;">
                <iframe id="iframe3_1" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe3_2" width="33%" height="500px" frameborder="0"></iframe>
                <iframe id="iframe3_3" width="33%" height="500px" frameborder="0"></iframe>
            </div>
        </div>

        <script>
            function updateIframes(cohortNumber) {{
                const cohort = document.getElementById('dropdown' + cohortNumber).value;
                const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                if (!cohort) {{
                    iframeContainer.style.display = 'none';  // Hide iframe container
                    document.getElementById('iframe' + cohortNumber + '_1').src = '';
                    document.getElementById('iframe' + cohortNumber + '_2').src = '';
                    document.getElementById('iframe' + cohortNumber + '_3').src = '';
                    return;
                }}

                iframeContainer.style.display = 'block';  // Show iframe container
                document.getElementById('iframe' + cohortNumber + '_1').src = `/html_files/member_access_by_state_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_2').src = `/html_files/service_usage_by_race_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_3').src = `/html_files/cost_by_race_${{cohort}}.html`;
            }}
        </script>
    </body>
    </html>
    """

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
