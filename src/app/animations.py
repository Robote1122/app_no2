import asyncio

class Animations:
    @staticmethod
    async def fade_in(widget, duration=0.3):
        """Плавное появление"""
        widget.style.opacity = 0
        await asyncio.sleep(0.1)
        widget.style.opacity = 1
    
    @staticmethod
    async def slide_in(widget, direction='right', duration=0.3):
        """Скользящее появление"""
        # Toga не поддерживает анимации напрямую,
        # но можно использовать этот метод как заглушку
        pass