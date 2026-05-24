from beartype import BeartypeConf
from beartype.claw import beartype_all

beartype_all(conf=BeartypeConf(
    is_pep484_tower=True,
))
