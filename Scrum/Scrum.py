from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from datetime import datetime


class ScrumService:
    """Servicio para gestionar la tabla de Scrum del proyecto."""

    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)
        self.scrum_file = self.data_dir / "scrum_board.json"
        self._ensure_scrum_file()

    def _ensure_scrum_file(self) -> None:
        """Crea el archivo scrum_board.json si no existe."""
        if not self.scrum_file.exists():
            initial_data = {
                "metadata": {
                    "grouped_mode": False,
                    "project_start_date": datetime.now().isoformat(),
                    "estimated_end_date": None,
                },
                "sprints": [
                    {
                        "id": "Spring 1",
                        "tareas": [
                            {
                                "titulo": "Crear UI",
                                "descripcion": "Diseñar la interfaz de usuario",
                                "tiempo_estimado_dias": 2,
                                "estado": "En Progreso",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            }
                        ]
                    },
                    {
                        "id": "Spring 2",
                        "tareas": [
                            {
                                "titulo": "Generar la etiqueta en un cuadro de dialogo",
                                "descripcion": "Implementar la generación de etiquetas",
                                "tiempo_estimado_dias": 1,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            },
                            {
                                "titulo": "Completar la plantilla para las etiquetas en PDF",
                                "descripcion": "Diseñar plantilla PDF",
                                "tiempo_estimado_dias": 1,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            },
                            {
                                "titulo": "Crear la etiqueta en png",
                                "descripcion": "Generar etiqueta en formato PNG",
                                "tiempo_estimado_dias": 1,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            }
                        ]
                    },
                    {
                        "id": "Spring 3",
                        "tareas": [
                            {
                                "titulo": "Colocar gráficas dentro del dashboard",
                                "descripcion": "Integrar visualización de datos en el dashboard",
                                "tiempo_estimado_dias": 1,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            }
                        ]
                    },
                    {
                        "id": "Spring 4",
                        "tareas": [
                            {
                                "titulo": "Mejorar UI de inicio de sesión",
                                "descripcion": "Optimizar la interfaz de login",
                                "tiempo_estimado_dias": 2,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            },
                            {
                                "titulo": "Asignar más formularios de acuerdo a la norma",
                                "descripcion": "Agregar formularios para normas 4, 20, 24, 50, 141, 189",
                                "tiempo_estimado_dias": 2,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            }
                        ]
                    },
                    {
                        "id": "Spring 5",
                        "tareas": [
                            {
                                "titulo": "Compilar a .exe y realizar pruebas",
                                "descripcion": "Compilación final y testing",
                                "tiempo_estimado_dias": 1,
                                "estado": "No Iniciado",
                                "asignado_a": "",
                                "fecha_inicio": None,
                                "fecha_fin": None,
                            }
                        ]
                    }
                ]
            }
            self._save_data(initial_data)

    def _load_data(self) -> dict[str, Any]:
        """Carga los datos del archivo JSON."""
        try:
            with open(self.scrum_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"sprints": []}

    def _save_data(self, data: dict[str, Any]) -> None:
        """Guarda los datos en el archivo JSON."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.scrum_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all_sprints(self) -> list[dict[str, Any]]:
        """Retorna todos los sprints."""
        data = self._load_data()
        return data.get("sprints", [])

    def get_sprint(self, sprint_id: str) -> dict[str, Any] | None:
        """Retorna un sprint específico por ID."""
        sprints = self.get_all_sprints()
        for sprint in sprints:
            if sprint.get("id") == sprint_id:
                return sprint
        return None

    def add_sprint(self, sprint_id: str) -> bool:
        """Añade un nuevo sprint."""
        data = self._load_data()
        if any(s.get("id") == sprint_id for s in data["sprints"]):
            return False
        data["sprints"].append({"id": sprint_id, "tareas": []})
        self._save_data(data)
        return True

    def add_tarea(self, sprint_id: str, tarea: dict[str, Any]) -> bool:
        """Añade una tarea a un sprint."""
        data = self._load_data()
        for sprint in data["sprints"]:
            if sprint.get("id") == sprint_id:
                tarea_default = {
                    "titulo": tarea.get("titulo", ""),
                    "descripcion": tarea.get("descripcion", ""),
                    "tiempo_estimado_dias": tarea.get("tiempo_estimado_dias", 0),
                    "estado": tarea.get("estado", "No Iniciado"),
                    "asignado_a": tarea.get("asignado_a", ""),
                    "fecha_inicio": tarea.get("fecha_inicio", None),
                    "fecha_fin": tarea.get("fecha_fin", None),
                }
                sprint["tareas"].append(tarea_default)
                self._save_data(data)
                return True
        return False

    def update_tarea(self, sprint_id: str, tarea_index: int, updates: dict[str, Any]) -> bool:
        """Actualiza una tarea específica."""
        data = self._load_data()
        for sprint in data["sprints"]:
            if sprint.get("id") == sprint_id:
                if 0 <= tarea_index < len(sprint["tareas"]):
                    sprint["tareas"][tarea_index].update(updates)
                    self._save_data(data)
                    return True
        return False

    def delete_tarea(self, sprint_id: str, tarea_index: int) -> bool:
        """Elimina una tarea específica."""
        data = self._load_data()
        for sprint in data["sprints"]:
            if sprint.get("id") == sprint_id:
                if 0 <= tarea_index < len(sprint["tareas"]):
                    del sprint["tareas"][tarea_index]
                    self._save_data(data)
                    return True
        return False

    def get_sprint_summary(self, sprint_id: str) -> dict[str, Any]:
        """Obtiene un resumen del sprint."""
        sprint = self.get_sprint(sprint_id)
        if not sprint:
            return {}

        tareas = sprint.get("tareas", [])
        total_tareas = len(tareas)
        tareas_completadas = sum(1 for t in tareas if t.get("estado") == "Completado")
        tareas_en_progreso = sum(1 for t in tareas if t.get("estado") == "En Progreso")
        tiempo_total = sum(t.get("tiempo_estimado_dias", 0) for t in tareas)

        return {
            "sprint_id": sprint_id,
            "total_tareas": total_tareas,
            "tareas_completadas": tareas_completadas,
            "tareas_en_progreso": tareas_en_progreso,
            "tareas_no_iniciadas": total_tareas - tareas_completadas - tareas_en_progreso,
            "tiempo_estimado_total": tiempo_total,
            "porcentaje_completado": (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0,
        }

    def get_project_summary(self) -> dict[str, Any]:
        """Obtiene un resumen del proyecto completo."""
        sprints = self.get_all_sprints()
        total_tareas = 0
        total_completadas = 0
        tiempo_total = 0

        for sprint in sprints:
            tareas = sprint.get("tareas", [])
            total_tareas += len(tareas)
            total_completadas += sum(1 for t in tareas if t.get("estado") == "Completado")
            tiempo_total += sum(t.get("tiempo_estimado_dias", 0) for t in tareas)

        return {
            "total_sprints": len(sprints),
            "total_tareas": total_tareas,
            "tareas_completadas": total_completadas,
            "tiempo_estimado_total_dias": tiempo_total,
            "porcentaje_completado": (total_completadas / total_tareas * 100) if total_tareas > 0 else 0,
        }

    # Métodos para manejar el estado de agrupamiento y fechas
    def get_grouped_mode(self) -> bool:
        """Obtiene el estado del modo agrupado."""
        data = self._load_data()
        metadata = data.get("metadata", {})
        return metadata.get("grouped_mode", False)
    
    def set_grouped_mode(self, grouped: bool) -> None:
        """Guarda el estado del modo agrupado."""
        data = self._load_data()
        if "metadata" not in data:
            data["metadata"] = {}
        data["metadata"]["grouped_mode"] = grouped
        self._save_data(data)
    
    def get_project_dates(self) -> dict[str, Any]:
        """Obtiene las fechas del proyecto."""
        data = self._load_data()
        metadata = data.get("metadata", {})
        
        start_date_str = metadata.get("project_start_date")
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else datetime.now()
        
        # Calcular fecha estimada de fin
        total_days = sum(
            t.get("tiempo_estimado_dias", 0)
            for sprint in data.get("sprints", [])
            for t in sprint.get("tareas", [])
        )
        
        estimated_end = start_date.timestamp() + (total_days * 86400)
        estimated_end_date = datetime.fromtimestamp(estimated_end)
        
        return {
            "start_date": start_date,
            "estimated_end_date": estimated_end_date,
            "total_estimated_days": total_days,
        }

