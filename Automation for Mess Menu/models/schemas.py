from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message describing the issue")

class CommonItems(BaseModel):
    Breakfast: str = Field(default="", description="Common items for Breakfast")
    Lunch: str = Field(default="", description="Common items for Lunch")
    Snacks: str = Field(default="", description="Common items for Snacks")
    Dinner: str = Field(default="", description="Common items for Dinner")

class MealSchedule(BaseModel):
    Breakfast: List[str] = Field(default_factory=list, description="Variable items for Breakfast")
    Lunch: List[str] = Field(default_factory=list, description="Variable items for Lunch")
    Snacks: List[str] = Field(default_factory=list, description="Variable items for Snacks")
    Dinner: List[str] = Field(default_factory=list, description="Variable items for Dinner")

class WeeklySchedule(BaseModel):
    schedule: Dict[str, MealSchedule] = Field(
        ...,
        description="Schedule for each day of the week",
        example={
            "Monday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Tuesday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Wednesday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Thursday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Friday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Saturday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []},
            "Sunday": {"Breakfast": [], "Lunch": [], "Snacks": [], "Dinner": []}
        }
    )

class MenuType(BaseModel):
    common_items: CommonItems = Field(default_factory=CommonItems, description="Common items for all days")
    A: WeeklySchedule = Field(default_factory=WeeklySchedule, description="Schedule for Week A")
    B: WeeklySchedule = Field(default_factory=WeeklySchedule, description="Schedule for Week B")
    C: WeeklySchedule = Field(default_factory=WeeklySchedule, description="Schedule for Week C")
    D: WeeklySchedule = Field(default_factory=WeeklySchedule, description="Schedule for Week D")

class MenuResponse(BaseModel):
    Unified_Veg: MenuType = Field(default_factory=MenuType, description="Menu for Unified Veg")
    Unified_Non_Veg: MenuType = Field(default_factory=MenuType, description="Menu for Unified Non-Veg")
    North_Veg: MenuType = Field(default_factory=MenuType, description="Menu for North Veg")
    North_Non_Veg: MenuType = Field(default_factory=MenuType, description="Menu for North Non-Veg")
    North_Veg_No_Onion_Garlic: MenuType = Field(default_factory=MenuType, description="Menu for North Veg No Onion Garlic")
    South_Veg: MenuType = Field(default_factory=MenuType, description="Menu for South Veg")
    South_Non_Veg: MenuType = Field(default_factory=MenuType, description="Menu for South Non-Veg")

class ProcessMenuRequest(BaseModel):
    file_type: Literal["pdf", "excel", "gsheet"] = Field(..., description="Type of files to process (pdf, excel, or gsheet)")