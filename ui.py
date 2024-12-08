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
    </head>
    <body>
        <h3>Select a Cohort to View Visualizations</h3>
        <select id="dropdown" onchange="updateIframes()">
            <option value="">Select Cohort</option>
            {dropdown}
        </select>
        <div style="display: flex; justify-content: space-between; margin-top: 20px;">
            <iframe id="iframe1" width="33%" height="500px" frameborder="0"></iframe>
            <iframe id="iframe2" width="33%" height="500px" frameborder="0"></iframe>
            <iframe id="iframe3" width="33%" height="500px" frameborder="0"></iframe>
        </div>
        <script>
            function updateIframes() {{
                const cohort = document.getElementById('dropdown').value;
                if (!cohort) {{
                    document.getElementById('iframe1').src = '';
                    document.getElementById('iframe2').src = '';
                    document.getElementById('iframe3').src = '';
                    return;
                }}
                document.getElementById('iframe1').src = `/html_files/member_access_by_state_${{cohort}}.html`;
                document.getElementById('iframe2').src = `/html_files/service_usage_by_race_${{cohort}}.html`;
                document.getElementById('iframe3').src = `/html_files/cost_by_race_${{cohort}}.html`;
            }}
        </script>
    </body>
    </html>
    """

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
