


"""
Śniadanie;
- zagotować wodę (0.3 sek); boil_water -> int
- zaparzyć kawę (potrzebuje wodę; 0.2 s); make_caffe –> cafee
- pokroić chleb (0.1 s); cut_bread -> bread
- posmarować masłem chleb (0.1 s); prepare_bread; wymaga "bread" -> good_bread
- zagotować jajka (0.4 s); boil_eggs; -> eggs
- przygotować stół (0.1 s); wymaga: cafee, good_bread, eggs


Zadanie -- napisać funkcje jak ↑↑, np. async def make_cafee(water: int) -> int

A) Napisać odpowiednie funkcje jak ↑↑
B) Napisać funckę async def scheduler, który wykona przygotowanie śnidania zgodnie z przepisem





"""