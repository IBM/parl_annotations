(define (problem logistics-c2-p2-0)
(:domain logistics)
(:objects
 apn1 - airplane
 apt1 apt2 - airport
 pos2 pos1 - location
 cit2 cit1 - city
 tru2 tru1 - truck
 obj21 obj11 - package)

(:init
    (at apn1 apt2)
    (at tru1 pos1)
    (at obj11 pos1)
    (at tru2 pos2)
    (at obj21 pos2)
    (IN-CITY pos1 cit1) (IN-CITY apt1 cit1) (IN-CITY pos2 cit2) (IN-CITY apt2 cit2))

(:goal (and
            (at obj11 pos2)
            (at obj21 pos1)
        ))
)