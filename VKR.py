# VKR.py
# Сетевая информационная система по детским инфекционным заболеваниям

from enum import Enum
from typing import List, Optional, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title="Информационная система по детским инфекционным заболеваниям",
    description=(
        "Учебный пример сетевой информационной системы, "
        "предоставляющей справочные данные о детских инфекционных "
        "заболеваниях, симптомах и упрощённой статистике."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# МОДЕЛИ ДАННЫХ
# ---------------------------------------------------------------------------


class Season(str, Enum):
    """Сезонность для эпидемиологической статистики."""
    winter = "Зима"
    spring = "Весна"
    summer = "Лето"
    autumn = "Осень"


class AgeGroup(str, Enum):
    """Возрастные группы (укрупнённая классификация)."""
    preschool = "Дошкольный возраст"
    under7 = "Дети до 7 лет"
    children = "Детский возраст"


class Symptom(BaseModel):
    """Симптом заболевания."""
    id: int
    name: str
    description: Optional[str] = None


class Disease(BaseModel):
    """Полное описание заболевания."""
    id: int
    name: str
    pathogen_type: str
    transmission: str
    age_group: AgeGroup
    symptoms: List[Symptom]
    prevention: Optional[str] = None


class DiseaseShort(BaseModel):
    """Короткое описание заболевания (для списков)."""
    id: int
    name: str
    age_group: AgeGroup
    pathogen_type: str


class StatisticItem(BaseModel):
    """Статистический показатель."""
    disease_id: int
    year: int
    season: Season
    cases: int = Field(..., ge=0)


class DiseaseWithStats(Disease):
    """Данные по заболеванию с сезонной статистикой."""
    statistics: List[StatisticItem]


# ---------------------------------------------------------------------------
# "БАЗА ДАННЫХ" В ПАМЯТИ
# ---------------------------------------------------------------------------

SYMPTOMS_DB: List[Symptom] = [
    Symptom(id=1, name="Лихорадка", description="Повышенная температура тела"),
    Symptom(id=2, name="Сыпь", description="Пятнистая или папулёзная сыпь"),
    Symptom(id=3, name="Кашель", description="Сухой или влажный кашель"),
    Symptom(id=4, name="Насморк", description="Выделения из носа"),
    Symptom(id=5, name="Головная боль", description="Боль различной интенсивности"),
    Symptom(id=6, name="Рвота", description="Обратное движение содержимого желудка"),
    Symptom(id=7, name="Диарея", description="Частый жидкий стул"),
    Symptom(id=8, name="Боль в горле", description="Воспаление слизистой горла"),
    Symptom(id=9, name="Конъюнктивит", description="Покраснение и воспаление глаз"),
    Symptom(id=10, name="Увеличение лимфоузлов", description="Лимфаденопатия"),
]

SYMPTOMS_BY_ID: Dict[int, Symptom] = {s.id: s for s in SYMPTOMS_DB}

DISEASES_DB: List[Disease] = [
    Disease(
        id=1,
        name="Корь",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.preschool,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[10]],
        prevention="Вакцинация по национальному календарю",
    ),
    Disease(
        id=2,
        name="Коклюш",
        pathogen_type="Бактерия",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.under7,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[3]],
        prevention="Вакцинация (АКДС)",
    ),
    Disease(
        id=3,
        name="Ветряная оспа",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[1]],
        prevention="Изоляция заболевших, вакцинация",
    ),
    Disease(
        id=4,
        name="Краснуха",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[9]],
        prevention="Вакцинация (КПК)",
    ),
    Disease(
        id=5,
        name="Скарлатина",
        pathogen_type="Бактерия",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[8], SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[1]],
        prevention="Своевременное назначение антибиотиков",
    ),
    Disease(
        id=6,
        name="Свинка (эпидемический паротит)",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[10]],
        prevention="Вакцинация (КПК)",
    ),
    Disease(
        id=7,
        name="Ротавирусная инфекция",
        pathogen_type="Вирус",
        transmission="Фекально-оральный",
        age_group=AgeGroup.under7,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[1]],
        prevention="Гигиена, оральная регидратация",
    ),
    Disease(
        id=8,
        name="Менингококковая инфекция",
        pathogen_type="Бактерия",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5], SYMPTOMS_BY_ID[10]],
        prevention="Немедленное начало лечения, вакцинация",
    ),
    Disease(
        id=9,
        name="Аденовирусная инфекция",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.preschool,
        symptoms=[SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[9]],
        prevention="Соблюдение гигиены, изоляция заболевших",
    ),
    Disease(
        id=10,
        name="Энтеровирусная инфекция",
        pathogen_type="Вирус",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена, контроль качества воды и пищи",
    ),
    Disease(
        id=11,
        name="Грипп",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5], SYMPTOMS_BY_ID[3]],
        prevention="Ежегодная вакцинация, изоляция заболевших",
    ),
    Disease(
        id=12,
        name="ОРВИ",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена и поддерживающая терапия",
    ),
    Disease(
        id=13,
        name="Ангина (острый тонзиллит)",
        pathogen_type="Бактерия",
        transmission="Контактный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[8], SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Рациональная антибактериальная терапия",
    ),
    Disease(
        id=14,
        name="Дифтерия",
        pathogen_type="Бактерия",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[8], SYMPTOMS_BY_ID[1]],
        prevention="Вакцинация (АКДС)",
    ),
    Disease(
        id=15,
        name="Пищевые токсикоинфекции",
        pathogen_type="Бактерии",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[7]],
        prevention="Соблюдение правил пищевой безопасности",
    ),
    # -------- дополнительные заболевания 16–45 --------
    Disease(
        id=16,
        name="Норовирусная инфекция",
        pathogen_type="Вирус",
        transmission="Фекально-оральный",
        age_group=AgeGroup.under7,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена рук, контроль качества пищи и воды",
    ),
    Disease(
        id=17,
        name="Коронавирусная инфекция (у детей)",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[4]],
        prevention="Гигиена, масочный режим в сезон подъёма заболеваемости",
    ),
    Disease(
        id=18,
        name="Парагрипп",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[1]],
        prevention="Изоляция заболевших, гигиена рук",
    ),
    Disease(
        id=19,
        name="Эпидемический конъюнктивит",
        pathogen_type="Вирус",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[9], SYMPTOMS_BY_ID[1]],
        prevention="Гигиена рук, индивидуальные полотенца",
    ),
    Disease(
        id=20,
        name="Инфекционный мононуклеоз",
        pathogen_type="Вирус",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[10], SYMPTOMS_BY_ID[5]],
        prevention="Ограничение бытовых контактов в период болезни",
    ),
    Disease(
        id=21,
        name="Цитомегаловирусная инфекция",
        pathogen_type="Вирус",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Соблюдение гигиены, обследование беременных",
    ),
    Disease(
        id=22,
        name="Сальмонеллёз",
        pathogen_type="Бактерия",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[1]],
        prevention="Термическая обработка продуктов, гигиена",
    ),
    Disease(
        id=23,
        name="Шигеллёз (бактериальная дизентерия)",
        pathogen_type="Бактерия",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Безопасная вода, санитарно-гигиенические мероприятия",
    ),
    Disease(
        id=24,
        name="Лямблиоз",
        pathogen_type="Паразит",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[5]],
        prevention="Кипячение воды, мытьё рук и овощей",
    ),
    Disease(
        id=25,
        name="Кишечная эшерихиозная инфекция",
        pathogen_type="Бактерия",
        transmission="Фекально-оральный",
        age_group=AgeGroup.under7,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[6]],
        prevention="Соблюдение санитарных норм, контроль питания детей",
    ),
    Disease(
        id=26,
        name="Герпетическая инфекция (простого герпеса)",
        pathogen_type="Вирус",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[8]],
        prevention="Исключение тесных контактов в период высыпаний",
    ),
    Disease(
        id=27,
        name="Вирусный гепатит А",
        pathogen_type="Вирус",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[6], SYMPTOMS_BY_ID[7]],
        prevention="Вакцинация, безопасная вода и пища",
    ),
    Disease(
        id=28,
        name="Вирусный гепатит B",
        pathogen_type="Вирус",
        transmission="Контактный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Вакцинация, одноразовые инструменты",
    ),
    Disease(
        id=29,
        name="Клещевой энцефалит",
        pathogen_type="Вирус",
        transmission="Трансмиссивный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Вакцинация, защита от клещей",
    ),
    Disease(
        id=30,
        name="Болезнь Лайма (боррелиоз)",
        pathogen_type="Бактерия",
        transmission="Трансмиссивный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[5], SYMPTOMS_BY_ID[10]],
        prevention="Защита от клещей, раннее удаление клеща",
    ),
    Disease(
        id=31,
        name="Стафилококковая кожная инфекция",
        pathogen_type="Бактерия",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[1]],
        prevention="Гигиена кожи, обработка микротравм",
    ),
    Disease(
        id=32,
        name="Импетиго",
        pathogen_type="Бактерия",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2]],
        prevention="Гигиена, изоляция ребёнка до заживления элементов",
    ),
    Disease(
        id=33,
        name="Педикулёз",
        pathogen_type="Паразит",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[5]],
        prevention="Регулярный осмотр волос, обработка головных уборов",
    ),
    Disease(
        id=34,
        name="Стрептодермия",
        pathogen_type="Бактерия",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2]],
        prevention="Гигиена, обработка кожных повреждений",
    ),
    Disease(
        id=35,
        name="Острый бронхит",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[1]],
        prevention="Избегать переохлаждения, санация очагов инфекции",
    ),
    Disease(
        id=36,
        name="Пневмония (бактериальная)",
        pathogen_type="Бактерия",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Вакцинация против пневмококка, своевременное лечение ОРВИ",
    ),
    Disease(
        id=37,
        name="Пневмония (вирусная)",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[3], SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[1]],
        prevention="Профилактика ОРВИ, изоляция заболевших",
    ),
    Disease(
        id=38,
        name="Острый синусит",
        pathogen_type="Бактерия",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[4], SYMPTOMS_BY_ID[5], SYMPTOMS_BY_ID[1]],
        prevention="Лечение ринита, профилактика переохлаждения",
    ),
    Disease(
        id=39,
        name="Острый средний отит",
        pathogen_type="Бактерия",
        transmission="Восходящий путь из носоглотки",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Лечение респираторных инфекций, защита ушей от воды",
    ),
    Disease(
        id=40,
        name="Вирусный фарингит",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[8], SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена, ограничение контактов в период заболеваемости",
    ),
    Disease(
        id=41,
        name="Мезаденит (вирусной этиологии)",
        pathogen_type="Вирус",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена питания и рук",
    ),
    Disease(
        id=42,
        name="Токсоплазмоз (у детей)",
        pathogen_type="Паразит",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[10], SYMPTOMS_BY_ID[5]],
        prevention="Термическая обработка мяса, гигиена при уходе за животными",
    ),
    Disease(
        id=43,
        name="Энтеробиоз (глистная инвазия)",
        pathogen_type="Паразит",
        transmission="Фекально-оральный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[7], SYMPTOMS_BY_ID[5]],
        prevention="Гигиена рук, коротко подстриженные ногти, обработка постельного белья",
    ),
    Disease(
        id=44,
        name="Кандидоз полости рта (молочница)",
        pathogen_type="Грибок",
        transmission="Контактно-бытовой",
        age_group=AgeGroup.preschool,
        symptoms=[SYMPTOMS_BY_ID[8]],
        prevention="Гигиена полости рта, стерильность сосок и бутылочек",
    ),
    Disease(
        id=45,
        name="Парвовирусная инфекция (инфекционная эритема)",
        pathogen_type="Вирус",
        transmission="Воздушно-капельный",
        age_group=AgeGroup.children,
        symptoms=[SYMPTOMS_BY_ID[2], SYMPTOMS_BY_ID[1], SYMPTOMS_BY_ID[5]],
        prevention="Изоляция заболевших, соблюдение гигиены",
    ),
]

# Сезонная статистика за несколько лет
STATISTICS_DB: List[StatisticItem] = []
YEARS = [2021, 2022, 2023]

for disease in DISEASES_DB:
    base = 25 + disease.id * 6
    for year in YEARS:
        year_coeff = 0.9 + 0.1 * (year - YEARS[0])  # 2021 -> 0.9, 2022 -> 1.0, 2023 -> 1.1
        base_year = int(base * year_coeff)

        if disease.transmission == "Воздушно-капельный":
            coeffs = {
                Season.winter: 1.5,
                Season.spring: 1.1,
                Season.summer: 0.6,
                Season.autumn: 1.0,
            }
        elif disease.transmission == "Фекально-оральный":
            coeffs = {
                Season.winter: 0.6,
                Season.spring: 0.9,
                Season.summer: 1.6,
                Season.autumn: 1.2,
            }
        else:
            coeffs = {
                Season.winter: 1.0,
                Season.spring: 1.1,
                Season.summer: 0.9,
                Season.autumn: 1.0,
            }

        for season, k in coeffs.items():
            STATISTICS_DB.append(
                StatisticItem(
                    disease_id=disease.id,
                    year=year,
                    season=season,
                    cases=int(base_year * k),
                )
            )

# ---------------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------


def get_disease_or_404(disease_id: int) -> Disease:
    for disease in DISEASES_DB:
        if disease.id == disease_id:
            return disease
    raise HTTPException(status_code=404, detail="Заболевание не найдено")


def attach_stats(disease: Disease) -> DiseaseWithStats:
    stats = [s for s in STATISTICS_DB if s.disease_id == disease.id]
    return DiseaseWithStats(**disease.model_dump(), statistics=stats)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------


@app.get("/diseases", response_model=List[DiseaseShort], tags=["Заболевания"])
def list_diseases(
    transmission: Optional[str] = Query(None, description="Механизм передачи"),
    age_group: Optional[AgeGroup] = Query(None, description="Возрастная группа"),
    pathogen_type: Optional[str] = Query(None, description="Тип возбудителя"),
    q: Optional[str] = Query(None, description="Поиск по названию"),
):
    result = DISEASES_DB

    if transmission:
        t = transmission.lower().strip()
        result = [d for d in result if d.transmission.lower() == t]

    if age_group:
        result = [d for d in result if d.age_group == age_group]

    if pathogen_type:
        p = pathogen_type.lower().strip()
        result = [d for d in result if d.pathogen_type.lower() == p]

    if q:
        query_norm = q.lower().strip()
        result = [d for d in result if query_norm in d.name.lower()]

    return [
        DiseaseShort(
            id=d.id,
            name=d.name,
            age_group=d.age_group,
            pathogen_type=d.pathogen_type,
        )
        for d in result
    ]


@app.get("/diseases/{disease_id}", response_model=DiseaseWithStats, tags=["Заболевания"])
def get_disease(disease_id: int):
    disease = get_disease_or_404(disease_id)
    return attach_stats(disease)


@app.get("/symptoms", response_model=List[Symptom], tags=["Симптомы"])
def list_symptoms():
    return SYMPTOMS_DB


@app.get("/search/by-symptom/{symptom_id}", response_model=List[DiseaseShort], tags=["Поиск"])
def search_by_symptom(symptom_id: int):
    result = [d for d in DISEASES_DB if any(s.id == symptom_id for s in d.symptoms)]
    if not result:
        raise HTTPException(status_code=404, detail="Нет заболеваний с данным симптомом")
    return [
        DiseaseShort(
            id=d.id,
            name=d.name,
            age_group=d.age_group,
            pathogen_type=d.pathogen_type,
        )
        for d in result
    ]


@app.get("/statistics", response_model=List[StatisticItem], tags=["Статистика"])
def get_statistics(
    year: Optional[int] = Query(None, description="Год наблюдения"),
    season: Optional[Season] = Query(None, description="Сезон"),
    disease_id: Optional[int] = Query(None, description="ID заболевания"),
):
    stats = STATISTICS_DB
    if year is not None:
        stats = [s for s in stats if s.year == year]
    if season is not None:
        stats = [s for s in stats if s.season == season]
    if disease_id is not None:
        stats = [s for s in stats if s.disease_id == disease_id]
    return stats


@app.get("/meta/filters", tags=["Служебные"])
def filter_meta() -> Dict[str, List[str]]:
    return {
        "age_groups": sorted({d.age_group.value for d in DISEASES_DB}),
        "transmissions": sorted({d.transmission for d in DISEASES_DB}),
        "pathogen_types": sorted({d.pathogen_type for d in DISEASES_DB}),
    }


# ---------------------------------------------------------------------------
# ВЕБ-ИНТЕРФЕЙС
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Система по детским инфекционным заболеваниям</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            :root {
                --blue: #2563eb;
                --blue-light: #e0edff;
                --bg: #f3f4f6;
                --text-muted: #6b7280;
                --card-bg: #ffffff;
                --text-main: #111827;
                --row-selected-bg: #dbeafe;
                --row-selected-border: #2563eb;
            }

            body.dark-theme {
                --blue: #38bdf8;
                --blue-light: rgba(56, 189, 248, 0.15);
                --bg: #020617;
                --card-bg: #020617;
                --text-muted: #9ca3af;
                --text-main: #e5e7eb;
                --row-selected-bg: #0b1120;
                --row-selected-border: #38bdf8;

                background:
                    radial-gradient(circle at 0% 0%, rgba(56,189,248,0.23), transparent 55%),
                    radial-gradient(circle at 100% 100%, rgba(37,99,235,0.27), transparent 60%),
                    #020617;
            }

            * { box-sizing: border-box; }

            body {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
                margin: 0;
                padding: 0;
                background:
                    radial-gradient(circle at 0% 0%, rgba(59,130,246,0.18), transparent 55%),
                    radial-gradient(circle at 100% 100%, rgba(56,189,248,0.18), transparent 60%),
                    var(--bg);
                color: var(--text-main);
                transition: background 0.25s ease, color 0.25s ease;
            }

            header {
                background: var(--blue);
                color: white;
                padding: 18px 24px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 16px;
                flex-wrap: wrap;
                position: relative;
                z-index: 2;
            }
            header h1 {
                margin: 0;
                font-size: 22px;
            }
            header p {
                margin: 0;
                font-size: 13px;
                opacity: 0.95;
            }
            .header-right {
                display: flex;
                align-items: center;
                gap: 12px;
                flex-wrap: wrap;
            }
            .theme-toggle {
                padding: 6px 10px;
                font-size: 13px;
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.6);
                background: rgba(15,23,42,0.15);
                color: white;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }
            .theme-toggle:hover {
                background: rgba(15,23,42,0.3);
            }

            .watermark {
                position: fixed;
                inset: 0;
                pointer-events: none;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 96px;
                font-weight: 800;
                color: rgba(148,163,184,0.18);
                z-index: 0;
                text-align: center;
                padding: 0 80px;
                line-height: 1.1;
            }
            body.dark-theme .watermark {
                color: rgba(31,41,55,0.5);
            }

            main { padding: 24px; position: relative; z-index: 1; }
            .layout {
                max-width: 1100px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 2fr 1fr;
                grid-gap: 16px;
                position: relative;
            }
            @media (max-width: 900px) {
                .layout { grid-template-columns: 1fr; }
            }
            .card {
                background: var(--card-bg);
                border-radius: 16px;
                box-shadow: 0 18px 40px rgba(15,23,42,0.12);
                padding: 18px 20px;
                transition: background 0.25s ease, box-shadow 0.25s ease, transform 0.15s ease;
            }
            body.dark-theme .card {
                box-shadow: 0 2px 12px rgba(0,0,0,0.6);
            }
            .card:hover {
                transform: translateY(-2px);
                box-shadow: 0 22px 50px rgba(15,23,42,0.16);
            }
            .card h2 {
                margin: 0 0 10px;
                font-size: 18px;
            }
            .card p {
                margin: 0 0 12px;
                font-size: 14px;
                color: var(--text-muted);
            }
            .filters {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 12px;
                align-items: center;
            }
            .filters input,
            .filters select {
                padding: 6px 10px;
                font-size: 14px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                min-width: 140px;
                background: #ffffff;
                color: #111827;
            }
            body.dark-theme .filters input,
            body.dark-theme .filters select {
                background: #020617;
                border-color: #1f2937;
                color: #e5e7eb;
            }
            .filters button {
                padding: 7px 14px;
                font-size: 14px;
                border-radius: 6px;
                border: none;
                cursor: pointer;
                background: var(--blue);
                color: white;
                transition: background 0.15s ease, transform 0.1s ease;
            }
            .filters button.secondary {
                background: #6b7280;
            }
            .filters button:hover {
                background: #1d4ed8;
                transform: translateY(-1px);
            }
            .filters button.secondary:hover { background: #4b5563; }
            .counter {
                font-size: 13px;
                margin-bottom: 6px;
            }
            .muted {
                color: var(--text-muted);
                font-size: 13px;
                margin-bottom: 6px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 4px;
                font-size: 14px;
            }
            th, td {
                padding: 8px 10px;
                border-bottom: 1px solid #e5e7eb;
                text-align: left;
            }
            body.dark-theme th,
            body.dark-theme td {
                border-color: #1f2937;
            }
            th {
                background: #f9fafb;
                font-weight: 600;
                font-size: 13px;
                cursor: pointer;
                user-select: none;
            }
            body.dark-theme th {
                background: #0f172a;
            }
            th.sort-asc::after {
                content: " ▲";
                font-size: 11px;
            }
            th.sort-desc::after {
                content: " ▼";
                font-size: 11px;
            }
            th:first-child,
            td:first-child {
                width: 50px;
                text-align: center;
            }

            tbody tr:nth-child(even) {
                background: #f9fafb;
            }
            body.dark-theme tbody tr:nth-child(even) {
                background: #020617;
            }

            tr:hover {
                background: #f3f4ff;
                cursor: pointer;
            }
            body.dark-theme tr:hover {
                background: #0b1120;
            }
            .row-selected {
                background: var(--row-selected-bg) !important;
                box-shadow: inset 4px 0 0 var(--row-selected-border);
                font-weight: 600;
            }

            .badge {
                display: inline-block;
                padding: 3px 9px;
                border-radius: 999px;
                background: var(--blue-light);
                color: #1d4ed8;
                font-size: 12px;
            }

            .badge-pathogen {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 3px 9px;
                border-radius: 999px;
                font-size: 12px;
            }
            .badge-virus {
                background: #dcfce7;
                color: #166534;
            }
            .badge-bacteria {
                background: #fef3c7;
                color: #92400e;
            }
            .badge-other {
                background: #e5e7eb;
                color: #374151;
            }
            body.dark-theme .badge-virus {
                background: rgba(22, 101, 52, 0.25);
                color: #bbf7d0;
            }
            body.dark-theme .badge-bacteria {
                background: rgba(146, 64, 14, 0.25);
                color: #fed7aa;
            }
            body.dark-theme .badge-other {
                background: #111827;
                color: #e5e7eb;
            }

            .details-title {
                font-weight: 600;
                margin-bottom: 6px;
            }
            .details-empty {
                font-size: 13px;
                color: var(--text-muted);
            }
            #details {
                opacity: 0;
                transform: translateY(6px);
                transition: opacity 0.25s ease, transform 0.25s ease;
            }
            #details.active {
                opacity: 1;
                transform: translateY(0);
            }
            .details-block {
                margin-bottom: 10px;
                font-size: 14px;
            }
            .details-label {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                font-weight: 600;
                min-width: 160px;
            }
            .details-label span.icon {
                font-size: 15px;
            }

            .pill {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                padding: 4px 8px;
                border-radius: 999px;
                background: rgba(37,99,235,0.06);
                border: 1px solid rgba(37,99,235,0.15);
                font-size: 12px;
                margin: 2px 4px 2px 0;
                transition: transform 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
            }
            .pill::before {
                content: "•";
                font-size: 12px;
            }
            .pill:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(15,23,42,0.18);
                background: rgba(37,99,235,0.12);
            }
            body.dark-theme .pill {
                background: rgba(56,189,248,0.12);
                border-color: rgba(56,189,248,0.4);
            }

            .toolbar {
                margin-top: 8px;
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }
            .toolbar button {
                padding: 5px 10px;
                font-size: 12px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background: #f9fafb;
                cursor: pointer;
                transition: background 0.15s ease, transform 0.1s ease;
            }
            .toolbar button:hover {
                background: #e5e7eb;
                transform: translateY(-1px);
            }
            body.dark-theme .toolbar button {
                background: #0f172a;
                border-color: #1f2937;
                color: #e5e7eb;
            }
            body.dark-theme .toolbar button:hover {
                background: #1f2937;
            }

            .selection-info {
                font-size: 13px;
                margin-bottom: 8px;
                color: #374151;
            }
            body.dark-theme .selection-info {
                color: #9ca3af;
            }

            #yearSelect {
                margin-top: 8px;
                margin-bottom: 4px;
                padding: 4px 8px;
                font-size: 13px;
                border-radius: 6px;
                border: 1px solid #d1d5db;
                background: #ffffff;
            }
            body.dark-theme #yearSelect {
                background: #020617;
                border-color: #1f2937;
                color: #e5e7eb;
            }

            #statsChart {
                opacity: 0;
                transform: translateY(6px);
                transition: opacity 0.25s ease, transform 0.25s ease;
            }
            #statsChart.visible {
                opacity: 1;
                transform: translateY(0);
            }
        </style>
    </head>
    <body>
        <header>
            <div>
                <h1>Сетевая информационная система по детским инфекционным заболеваниям</h1>
                <p>Разработано Соловьевой Мариной Андреевной</p>
            </div>
            <div class="header-right">
                <button id="themeToggle" class="theme-toggle" onclick="toggleTheme()">🌙 Тёмная тема</button>
            </div>
        </header>

        <div class="watermark">
            🧸 Детские инфекционные заболевания
        </div>

        <main>
            <div class="layout">
                <div class="card">
                    <h2>Справочник заболеваний</h2>
                    <p>Используйте строку поиска и фильтры, чтобы отобрать интересующие заболевания.</p>
                    <div class="filters">
                        <input id="search" type="text" placeholder="Поиск по названию..." />
                        <select id="ageGroup">
                            <option value="">Все возрастные группы</option>
                        </select>
                        <select id="transmission">
                            <option value="">Все механизмы передачи</option>
                        </select>
                        <select id="symptomFilter">
                            <option value="">Все симптомы</option>
                        </select>
                        <!-- Кнопка "Применить" убрана, остаётся только "Сброс" -->
                        <button class="secondary" onclick="resetFilters()">Сброс</button>
                    </div>
                    <div id="counter" class="counter"></div>
                    <div class="muted">
                        Можно отфильтровать по возрасту, механизму передачи или отдельному симптому.
                        Кликните по строке в таблице, чтобы увидеть подробное описание.
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th id="th-id" data-col="id">ID</th>
                                <th id="th-name" data-col="name">Заболевание</th>
                                <th>Возбудитель</th>
                                <th style="width:220px;">Возрастная группа</th>
                            </tr>
                        </thead>
                        <tbody id="tableBody">
                            <tr><td colspan="4">Загрузка...</td></tr>
                        </tbody>
                    </table>
                    <div class="toolbar">
                        <button onclick="exportData('csv')">Экспорт в CSV</button>
                        <button onclick="exportData('json')">Экспорт в JSON</button>
                    </div>
                </div>
                <div class="card">
                    <h2>Подробная информация</h2>
                    <div id="selectionInfo" class="selection-info">
                        Заболевание не выбрано.
                    </div>
                    <div id="details">
                        <div class="details-empty">
                            Выберите заболевание в таблице слева, чтобы посмотреть подробности:
                            возбудитель, путь передачи, симптомы и сезонную статистику за несколько лет.
                        </div>
                    </div>
                    <select id="yearSelect" style="display:none;"></select>
                    <canvas id="statsChart" width="400" height="220" style="margin-top: 8px; display:none;"></canvas>
                </div>
            </div>
        </main>

        <script>
            let statsChart = null;
            let totalCount = 45; // всего заболеваний
            let lastData = [];
            let sortState = { column: 'id', direction: 'asc' };
            let currentDisease = null;
            let currentYear = null;
            let selectedId = null;

            // ----------- ТЁМНАЯ / СВЕТЛАЯ ТЕМА -----------

            function updateThemeToggleText() {
                const btn = document.getElementById("themeToggle");
                if (!btn) return;
                if (document.body.classList.contains("dark-theme")) {
                    btn.textContent = "☀️ Светлая тема";
                } else {
                    btn.textContent = "🌙 Тёмная тема";
                }
            }

            function toggleTheme() {
                document.body.classList.toggle("dark-theme");
                const isDark = document.body.classList.contains("dark-theme");
                localStorage.setItem("theme", isDark ? "dark" : "light");
                updateThemeToggleText();
            }

            function initTheme() {
                const saved = localStorage.getItem("theme");
                if (saved === "dark") {
                    document.body.classList.add("dark-theme");
                }
                updateThemeToggleText();
            }

            // ----------- debounce для поля поиска -----------

            function debounce(fn, delay) {
                let timeout;
                return function(...args) {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => fn.apply(this, args), delay);
                };
            }

            // ---------------- Загрузка справочных данных для фильтров ----------------

            async function loadFilters() {
                try {
                    const [metaResp, sympResp] = await Promise.all([
                        fetch("/meta/filters"),
                        fetch("/symptoms")
                    ]);

                    if (metaResp.ok) {
                        const meta = await metaResp.json();
                        const ageSelect = document.getElementById("ageGroup");
                        const trSelect = document.getElementById("transmission");

                        meta.age_groups.forEach(value => {
                            const opt = document.createElement("option");
                            opt.value = value;
                            opt.textContent = value;
                            ageSelect.appendChild(opt);
                        });

                        meta.transmissions.forEach(value => {
                            const opt = document.createElement("option");
                            opt.value = value;
                            opt.textContent = value;
                            trSelect.appendChild(opt);
                        });
                    }

                    if (sympResp.ok) {
                        const symptoms = await sympResp.json();
                        const symSelect = document.getElementById("symptomFilter");
                        symptoms.forEach(s => {
                            const opt = document.createElement("option");
                            opt.value = s.id;
                            opt.textContent = s.name;
                            symSelect.appendChild(opt);
                        });
                    }

                    // подписываемся на изменения фильтров после их создания
                    const searchInput = document.getElementById("search");
                    const ageSelect = document.getElementById("ageGroup");
                    const trSelect = document.getElementById("transmission");
                    const symSelect = document.getElementById("symptomFilter");

                    const debouncedLoad = debounce(loadDiseases, 300);
                    searchInput.addEventListener("input", debouncedLoad);
                    ageSelect.addEventListener("change", loadDiseases);
                    trSelect.addEventListener("change", loadDiseases);
                    symSelect.addEventListener("change", loadDiseases);
                } catch (e) {
                    console.error("Ошибка загрузки фильтров", e);
                }
            }

            // ---------------- Загрузка списка заболеваний ----------------

            async function loadDiseases() {
                const symptomId = document.getElementById("symptomFilter").value;
                if (symptomId) {
                    await loadDiseasesBySymptom(symptomId);
                } else {
                    await loadDiseasesStandard();
                }
                applySorting();
                renderTable();
            }

            async function loadDiseasesStandard() {
                const q = document.getElementById("search").value.trim();
                const age = document.getElementById("ageGroup").value;
                const tr = document.getElementById("transmission").value;

                const params = new URLSearchParams();
                if (q) params.append("q", q);
                if (age) params.append("age_group", age);
                if (tr) params.append("transmission", tr);

                const url = "/diseases" + (params.toString() ? "?" + params.toString() : "");
                const response = await fetch(url);
                const data = await response.json();
                lastData = data;
                updateCounter("Найдено записей: " + data.length + " из " + totalCount);
            }

            async function loadDiseasesBySymptom(symptomId) {
                const response = await fetch("/search/by-symptom/" + symptomId);
                if (!response.ok) {
                    lastData = [];
                    updateCounter("По выбранному симптому заболевания не найдены.");
                    renderTable();
                    return;
                }
                const data = await response.json();
                lastData = data;
                updateCounter("Найдено по выбранному симптому: " + data.length + " из " + totalCount);
            }

            function updateCounter(text) {
                document.getElementById("counter").textContent = text;
            }

            // ---------------- Сортировка таблицы ----------------

            function applySorting() {
                if (!lastData || !lastData.length) return;
                const col = sortState.column;
                const dir = sortState.direction === 'asc' ? 1 : -1;

                lastData.sort((a, b) => {
                    let va = a[col];
                    let vb = b[col];
                    if (col === 'name') {
                        va = va.toLowerCase();
                        vb = vb.toLowerCase();
                    }
                    if (va < vb) return -1 * dir;
                    if (va > vb) return 1 * dir;
                    return 0;
                });
            }

            function setSort(column) {
                if (sortState.column === column) {
                    sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    sortState.column = column;
                    sortState.direction = 'asc';
                }
                applySorting();
                updateSortHeaderStyles();
                renderTable();
            }

            function updateSortHeaderStyles() {
                const thId = document.getElementById("th-id");
                const thName = document.getElementById("th-name");
                thId.classList.remove("sort-asc", "sort-desc");
                thName.classList.remove("sort-asc", "sort-desc");

                const target = sortState.column === 'id' ? thId : thName;
                target.classList.add(sortState.direction === 'asc' ? "sort-asc" : "sort-desc");
            }

            // ---------------- Вспомогательные функции ----------------

            function getPathogenClass(type) {
                const t = (type || "").toLowerCase();
                if (t.includes("вирус")) return "badge-virus";
                if (t.includes("бактер")) return "badge-bacteria";
                return "badge-other";
            }

            function getAgeLabel(age) {
                if (!age) return age;
                if (age.includes("Дошкольный")) return "👶 " + age;
                if (age.includes("до 7")) return "🧒 " + age;
                return "🧑‍🎓 " + age;
            }

            // ---------------- Отрисовка таблицы ----------------

            function onRowClick(id) {
                selectedId = id;
                renderTable();
                loadDiseaseDetails(id);
            }

            function renderTable() {
                const tbody = document.getElementById("tableBody");
                tbody.innerHTML = "";

                if (!lastData || !lastData.length) {
                    const row = document.createElement("tr");
                    const cell = document.createElement("td");
                    cell.colSpan = 4;
                    cell.textContent = "Ничего не найдено.";
                    row.appendChild(cell);
                    tbody.appendChild(row);
                    return;
                }

                lastData.forEach(item => {
                    const row = document.createElement("tr");
                    if (selectedId === item.id) {
                        row.classList.add("row-selected");
                    }

                    const idCell = document.createElement("td");
                    idCell.textContent = item.id;

                    const nameCell = document.createElement("td");
                    nameCell.textContent = item.name;

                    const pathogenCell = document.createElement("td");
                    const pSpan = document.createElement("span");
                    pSpan.className = "badge-pathogen " + getPathogenClass(item.pathogen_type);
                    pSpan.textContent = item.pathogen_type;
                    pathogenCell.appendChild(pSpan);

                    const ageCell = document.createElement("td");
                    const span = document.createElement("span");
                    span.className = "badge";
                    span.textContent = getAgeLabel(item.age_group);
                    ageCell.appendChild(span);

                    row.appendChild(idCell);
                    row.appendChild(nameCell);
                    row.appendChild(pathogenCell);
                    row.appendChild(ageCell);

                    row.addEventListener("click", () => onRowClick(item.id));

                    tbody.appendChild(row);
                });
            }

            // ---------------- Экспорт данных ----------------

            function exportData(format) {
                if (!lastData || !lastData.length) {
                    alert("Нет данных для экспорта");
                    return;
                }
                if (format === "json") {
                    const blob = new Blob([JSON.stringify(lastData, null, 2)], {type: "application/json"});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "diseases.json";
                    a.click();
                    URL.revokeObjectURL(url);
                } else if (format === "csv") {
                    const header = ["id", "name", "pathogen_type", "age_group"];
                    const rows = lastData.map(d => [d.id, d.name, d.pathogen_type, d.age_group]);
                    const csvLines = [header.join(";")].concat(rows.map(r => r.join(";")));
                    const blob = new Blob([csvLines.join("\\n")], {type: "text/csv;charset=utf-8;"});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "diseases.csv";
                    a.click();
                    URL.revokeObjectURL(url);
                }
            }

            // ---------------- Подробная информация и график ----------------

            async function loadDiseaseDetails(id) {
                const container = document.getElementById("details");
                const chartCanvas = document.getElementById("statsChart");
                const selectionInfo = document.getElementById("selectionInfo");
                const yearSelect = document.getElementById("yearSelect");

                container.classList.remove("active");
                container.innerHTML = "<div class='details-empty'>Загрузка подробной информации...</div>";

                chartCanvas.classList.remove("visible");

                const response = await fetch("/diseases/" + id);
                if (!response.ok) {
                    container.innerHTML = "<div class='details-empty'>Ошибка загрузки данных.</div>";
                    chartCanvas.style.display = "none";
                    yearSelect.style.display = "none";
                    if (statsChart) { statsChart.destroy(); statsChart = null; }
                    selectionInfo.textContent = "Заболевание не выбрано.";
                    return;
                }

                const d = await response.json();
                currentDisease = d;

                selectionInfo.textContent = "Выбрано заболевание: " + d.name + " (ID: " + d.id + ")";

                const years = Array.from(new Set(d.statistics.map(s => s.year))).sort();
                yearSelect.innerHTML = "";
                years.forEach(y => {
                    const opt = document.createElement("option");
                    opt.value = y;
                    opt.textContent = "Год: " + y;
                    yearSelect.appendChild(opt);
                });
                if (years.length) {
                    yearSelect.style.display = "inline-block";
                    currentYear = years[years.length - 1];
                    yearSelect.value = currentYear;
                    yearSelect.onchange = () => {
                        currentYear = parseInt(yearSelect.value);
                        renderDetailsAndChart();
                    };
                } else {
                    yearSelect.style.display = "none";
                    currentYear = null;
                }

                renderDetailsAndChart();
            }

            function renderDetailsAndChart() {
                const d = currentDisease;
                const container = document.getElementById("details");
                const chartCanvas = document.getElementById("statsChart");

                if (!d) return;

                const yearFiltered = currentYear
                    ? d.statistics.filter(s => s.year === currentYear)
                    : d.statistics;

                const seasonOrder = { "Зима": 0, "Весна": 1, "Лето": 2, "Осень": 3 };
                const statsSorted = [...yearFiltered].sort((a, b) => {
                    const sa = seasonOrder[a.season] ?? 0;
                    const sb = seasonOrder[b.season] ?? 0;
                    return sa - sb;
                });

                const symptoms = d.symptoms
                    .map(s => "<span class='pill'>" + s.name + "</span>")
                    .join(" ");

                let statsHtml = "";
                if (statsSorted && statsSorted.length) {
                    statsHtml = statsSorted
                        .map(s => "<div class='pill'>" + s.season + " " + s.year + ": " + s.cases + "</div>")
                        .join("");
                } else {
                    statsHtml = "<span class='details-empty'>Статистические данные отсутствуют.</span>";
                }

                const pathogenClass = getPathogenClass(d.pathogen_type);

                container.innerHTML = `
                    <div class="details-title">${d.name}</div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">🧒</span><span>Возрастная группа:</span></span>
                        <span class="badge">${getAgeLabel(d.age_group)}</span>
                    </div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">🦠</span><span>Возбудитель:</span></span>
                        <span class="badge-pathogen ${pathogenClass}">${d.pathogen_type}</span>
                    </div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">🛣</span><span>Путь передачи:</span></span>
                        <span>${d.transmission}</span>
                    </div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">🤒</span><span>Симптомы:</span></span><br/>
                        ${symptoms}
                    </div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">🛡</span><span>Профилактика:</span></span><br/>
                        ${d.prevention || "Не указано"}
                    </div>
                    <div class="details-block">
                        <span class="details-label"><span class="icon">📊</span><span>Условная статистика:</span></span><br/>
                        ${statsHtml}
                    </div>
                `;

                requestAnimationFrame(() => {
                    container.classList.add("active");
                });

                if (statsSorted && statsSorted.length) {
                    const labels = statsSorted.map(s => s.season);
                    const values = statsSorted.map(s => s.cases);
                    const maxVal = Math.max(...values);
                    const percents = values.map(v => Math.round(v / maxVal * 100));

                    chartCanvas.style.display = "block";

                    if (statsChart) {
                        statsChart.destroy();
                    }

                    const ctx = chartCanvas.getContext("2d");
                    statsChart = new Chart(ctx, {
                        type: "bar",
                        data: {
                            labels: labels,
                            datasets: [
                                {
                                    type: "bar",
                                    label: "Число случаев",
                                    data: values,
                                    borderWidth: 1,
                                    yAxisID: "y",
                                },
                                {
                                    type: "line",
                                    label: "Доля от максимума, %",
                                    data: percents,
                                    borderWidth: 2,
                                    fill: false,
                                    yAxisID: "y1",
                                }
                            ]
                        },
                        options: {
                            interaction: { mode: "index", intersect: false },
                            animation: {
                                duration: 700,
                                easing: "easeOutQuart"
                            },
                            plugins: {
                                legend: { display: true },
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: { precision: 0 },
                                    title: { display: true, text: "Число случаев" }
                                },
                                y1: {
                                    position: "right",
                                    beginAtZero: true,
                                    min: 0,
                                    max: 110,
                                    ticks: {
                                        callback: (value) => value + "%"
                                    },
                                    grid: { drawOnChartArea: false },
                                    title: { display: true, text: "% от максимума" }
                                }
                            }
                        }
                    });

                    chartCanvas.classList.remove("visible");
                    requestAnimationFrame(() => {
                        chartCanvas.classList.add("visible");
                    });
                } else {
                    chartCanvas.style.display = "none";
                    chartCanvas.classList.remove("visible");
                    if (statsChart) { statsChart.destroy(); statsChart = null; }
                }
            }

            // ---------------- Сброс ----------------

            function resetFilters() {
                document.getElementById("search").value = "";
                document.getElementById("ageGroup").value = "";
                document.getElementById("transmission").value = "";
                document.getElementById("symptomFilter").value = "";
                selectedId = null;
                loadDiseases();
            }

            // ---------------- Инициализация ----------------

            document.getElementById("th-id").addEventListener("click", () => setSort("id"));
            document.getElementById("th-name").addEventListener("click", () => setSort("name"));
            updateSortHeaderStyles();

            initTheme();
            loadFilters().then(loadDiseases);
        </script>
    </body>
    </html>s
    """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("VKR:app", host="127.0.0.1", port=8001, reload=True)