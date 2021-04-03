def server_dev():
    import uvicorn
    uvicorn.run("scaip_gateway.api:app", host='0.0.0.0', port=8000, reload=False)
    