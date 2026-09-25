SCENARIOS = {
    "database_degradation": {
        "metrics": {
            "error_rate": 18.2,
            "baseline_error_rate": 2.1,
            "request_rate": 1240,
            "latency_p95_ms": 840,
        },
        "logs": [
            {
                "timestamp": "10:42:13",
                "level": "ERROR",
                "message": "Database connection timeout",
            },
            {
                "timestamp": "10:42:27",
                "level": "ERROR",
                "message": "Failed to acquire database connection",
            },
        ],
        "deployments": [
            {
                "version": "checkout-v41",
                "timestamp": "08:30",
                "status": "success",
            }
        ],
        "dependencies": {
            "postgres": {
                "status": "degraded",
                "latency_ms": 920,
            },
            "redis": {
                "status": "healthy",
                "latency_ms": 4,
            },
        },
    },
    "bad_deployment": {
        "metrics": {
            "error_rate": 15.7,
            "baseline_error_rate": 1.9,
            "request_rate": 1180,
            "latency_p95_ms": 690,
        },
        "logs": [
            {
                "timestamp": "11:07:21",
                "level": "ERROR",
                "message": "NullPointerException in checkout validation",
            },
            {
                "timestamp": "11:08:02",
                "level": "ERROR",
                "message": "Checkout request processing failed",
            },
        ],
        "deployments": [
            {
                "version": "checkout-v42",
                "timestamp": "11:02",
                "status": "success",
            }
        ],
        "dependencies": {
            "postgres": {
                "status": "healthy",
                "latency_ms": 12,
            },
            "redis": {
                "status": "healthy",
                "latency_ms": 4,
            },
        },
    },
    "redis_outage": {
        "metrics": {
            "error_rate": 12.4,
            "baseline_error_rate": 2.0,
            "request_rate": 1210,
            "latency_p95_ms": 610,
        },
        "logs": [
            {
                "timestamp": "12:14:11",
                "level": "ERROR",
                "message": "Redis connection refused",
            },
            {
                "timestamp": "12:14:29",
                "level": "ERROR",
                "message": "Cache operation failed",
            },
        ],
        "deployments": [
            {
                "version": "checkout-v41",
                "timestamp": "08:30",
                "status": "success",
            }
        ],
        "dependencies": {
            "postgres": {
                "status": "healthy",
                "latency_ms": 14,
            },
            "redis": {
                "status": "down",
                "latency_ms": 0,
            },
        },
    },
    "payment_timeout": {
        "metrics": {
            "error_rate": 10.8,
            "baseline_error_rate": 1.7,
            "request_rate": 1160,
            "latency_p95_ms": 970,
        },
        "logs": [
            {
                "timestamp": "13:21:44",
                "level": "ERROR",
                "message": "Payment provider request timeout",
            },
            {
                "timestamp": "13:22:03",
                "level": "ERROR",
                "message": "Payment confirmation failed",
            },
        ],
        "deployments": [
            {
                "version": "checkout-v41",
                "timestamp": "08:30",
                "status": "success",
            }
        ],
        "dependencies": {
            "postgres": {
                "status": "healthy",
                "latency_ms": 15,
            },
            "redis": {
                "status": "healthy",
                "latency_ms": 5,
            },
            "payment_provider": {
                "status": "degraded",
                "latency_ms": 1800,
            },
        },
    },
    "ambiguous_incident": {
        "metrics": {
            "error_rate": 7.1,
            "baseline_error_rate": 3.8,
            "request_rate": 1200,
            "latency_p95_ms": 410,
        },
        "logs": [
            {
                "timestamp": "14:10:11",
                "level": "ERROR",
                "message": "Request processing failed",
            },
            {
                "timestamp": "14:12:47",
                "level": "WARN",
                "message": "Temporary downstream latency detected",
            },
        ],
        "deployments": [
            {
                "version": "checkout-v42",
                "timestamp": "13:55",
                "status": "success",
            }
        ],
        "dependencies": {
            "postgres": {
                "status": "healthy",
                "latency_ms": 18,
            },
            "redis": {
                "status": "healthy",
                "latency_ms": 6,
            },
            "payment_provider": {
                "status": "healthy",
                "latency_ms": 120,
            },
        },
    },
}

CURRENT_SCENARIO = "database_degradation"


def get_current_scenario() -> dict:
    return SCENARIOS[CURRENT_SCENARIO]