class VideoOpsError(RuntimeError):
    """Base class for expected VideoOps failures."""


class ConflictError(VideoOpsError):
    """The requested state transition conflicts with current state."""


class NotFoundError(VideoOpsError):
    """A requested local resource does not exist."""


class PolicyError(VideoOpsError):
    """A fail-closed local policy rejected the operation."""


class BudgetExceeded(VideoOpsError):
    """A configured per-job budget was exhausted."""


class Cancelled(VideoOpsError):
    """A job was cancelled between bounded stage operations."""

