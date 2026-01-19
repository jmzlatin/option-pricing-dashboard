def get_custom_css():
    return """
    <style>
    .metric-card {
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .call-card {
        background-color: #e6fffa; /* Light Green */
        border: 2px solid #38b2ac;
    }
    .put-card {
        background-color: #fff5f5; /* Light Red */
        border: 2px solid #fc8181;
    }
    .metric-label {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
        color: #4a4a4a; 
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
    """
