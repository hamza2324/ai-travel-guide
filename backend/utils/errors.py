class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "app_error"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code


class LocationNotFoundError(AppError):
    def __init__(self, location: str):
        super().__init__(
            f"We couldn't find “{location}”. Try a city, region, or landmark name.",
            status_code=404,
            code="location_not_found",
        )


class PlacesNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            "We found fewer places than expected for this area. Try expanding your interests or adjusting the travel radius.",
            status_code=404,
            code="places_not_found",
        )


class AIServiceError(AppError):
    def __init__(self, message: str | None = None):
        super().__init__(
            message
            or "The AI planner is temporarily unavailable. Your trip can still be built from location data.",
            status_code=503,
            code="ai_unavailable",
        )
