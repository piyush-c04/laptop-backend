from pydantic import BaseModel
from typing import Optional,List

from src.api_schemas.review import ReviewResponse
# ======================
# LAPTOP SCHEMAS
# ======================

class LaptopBase(BaseModel):
    brand: str
    model: str
    price: int
    ram: str
    storage: str
    usage_type: str
    battery_life: str
    processor: str
    cpu: str
    gpu: str
    screensize: str
    processor_gen: str
    os: str
    office: str
    warranty: str
    refresh_rate: str
    weight_kg: str
    ram_speed: str
    storage_type: str
    storage_size: str
    screen_type: str
    resolution: str
    usb_ports: str
    hdmi_ports: str
    thunderbolt_ports: str
    audio_jack: str
    lan_port: str
    wifi: str
    fanspeed: str
    keyboard_light: str
    webcam: str
    webcam_resolution: str
    microphone: str
    speakers: str
    color: str
    launchdate: str
    image_url: str
    buy_link: str

    
class LaptopCreate(LaptopBase):
    pass

class LaptopUpdate(LaptopBase):
    pass

class LaptopResponse(LaptopBase):
    id: int
    reviews: List[ReviewResponse] = []
    avg_rating: Optional[str] = None
    
    model_config = {
        "from_attributes": True
    }