from datetime import timedelta

from schema import Schema, And, Use


switches = Schema({
    And(Use(unicode), len): And(
        Use(lambda d: timedelta(**d)),
        lambda td: td > timedelta()
    )
})
