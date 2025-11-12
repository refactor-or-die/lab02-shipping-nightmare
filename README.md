# Lab 02: Shipping Nightmare

## Czy wiesz, że...
Przeciętny programista spędza 73% czasu na debugowaniu if-ów w kodzie legacy? (źródło: there is no source, go to church)

## Twoje zadanie
Otrzymałeś kod kalkulatora kosztów wysyłki w e-commerce. Poprzedni developer uciekł w Bieszczady i zostawił po sobie metodę z **ponad 200 liniami if-ów**. 

Twój szef krzyczy: "Musimy dodać wysyłkę balonem na ogrzane powietrze!" 
Ty patrzysz na kod i myślisz: "Gdzie ja to wcisnę?"

**Rozwiązanie:** Wzorzec Strategy!

## Co zawiera repozytorium
- `shipping_calculator.py` - koszmar każdego programisty
- `test_shipping_calculator.py` - testy (NIE RUSZAĆ!)
- Ten README
- Cośtam jeszcze

## Instrukcja
1. Sklonuj repo i stwórz branch `lab2_nazwisko1_nazwisko2`
2. Uruchom testy: `pytest` (powinny przejść)
3. Zrefaktoryzuj kod używając wzorca Strategy
4. Uruchom testy ponownie (MUSZĄ przejść)
5. Commit + push na swój branch
6. Przygotuj się do prezentacji

## Wskazówki
- Każdy typ wysyłki (`standard`, `express`, itd.) powinien być osobną strategią
- Nie zmieniaj API metody `calculate_shipping()` - testy muszą działać!
- Pamiętaj o edge case'ach (np. drone nie lata w złą pogodę)
- If-ów w nowym kodzie powinno być maksymalnie kilka (nie 200!)

## Co zyskasz?
- Kod, który da się czytać bez płaczu
- Łatwość dodania nowego typu dostawy
- Możliwość testowania każdej strategii osobno
- Szacunek kolegów z zespołu

## Kryteria oceny
- Testy przechodzą
- Użyty wzorzec Strategy
- Kod jest czytelny
- Można łatwo dodać nowy typ wysyłki
- Prezentacja była zrozumiała

## FAQ
**Q: Czy mogę użyć Javy?**

A: Nie.

**Q: Czy mogę użyć bibliotek zewnętrznych?**

A: Nie potrzebujesz. Python ma wszystko (ABC, type hints).

**Q: Co z tą losowością w drone?**

A: Zostaw ją. Drony nie lubią deszczu.

**Q: 200 linii to dużo?**

A: Widziałem metodę z 2000 linii. Miała 47 poziomów zagnieżdżenia if-ów. Programista, który to napisał, teraz hoduje alpaki (serio).

**Q: Serio nie mogę użyć Javy?**

A: Nie.

**Q: Python jest po&#@%!!!**

A: Be my guest i spróbuj JavaScript, Perla albo PHP (ale nie na zajęciach).

**Q: To może spróbuję Javy???**

A: Nie.

**Q: Ale głupi ten prowadzący, każe używać Pythona a sam go nie zna?**

A: Nie mam potrzeby udawać wszystkowiedzącego. Poza tym - "nikt tu nikogo pod pistoletem nie trzyma" :)

---

*"Dobry kod to taki, który możesz zrozumieć o 3 w nocy po 4 piwach"* - Mądry Senior Developer (jest jak świnka morska)

Powodzenia!
