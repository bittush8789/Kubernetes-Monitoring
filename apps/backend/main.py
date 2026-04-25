from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = FastAPI(title="SRE Monitoring Demo API")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "api_requests_total", "Total count of requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds", "Request latency in seconds", ["method", "endpoint"]
)
ERROR_COUNT = Counter(
    "api_errors_total", "Total count of errors", ["method", "endpoint", "error_type"]
)

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        process_time = time.time() - start_time
        
        # Update metrics
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(process_time)
        
        return response
    except Exception as e:
        ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=type(e).__name__).inc()
        raise e

@app.get("/")
async def root():
    return {"message": "SRE Monitoring API is Online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/v1/data")
async def get_data():
    # Simulate variable latency
    time.sleep(random.uniform(0.01, 0.5))
    if random.random() < 0.05:
        # Simulate 5% error rate
        return Response(content='{"error": "Internal Server Error"}', status_code=500)
    return {"data": "Production metrics simulation"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
