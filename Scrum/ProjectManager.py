"""Gestor de proyectos Scrum - permite crear y manejar múltiples proyectos."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any
from datetime import datetime
from ProjectTemplates import get_template


class ProjectManager:
    """Gestiona múltiples proyectos Scrum."""

    def __init__(self, base_dir: str | Path = "projects") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.base_dir / "projects_index.json"
        self._ensure_projects_index()

    def _ensure_projects_index(self) -> None:
        """Crea el archivo de índice de proyectos si no existe."""
        if not self.projects_file.exists():
            initial_data = {
                "projects": [],
                "last_opened": None,
            }
            self._save_index(initial_data)

    def _load_index(self) -> dict[str, Any]:
        """Carga el índice de proyectos."""
        try:
            with open(self.projects_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"projects": [], "last_opened": None}

    def _save_index(self, data: dict[str, Any]) -> None:
        """Guarda el índice de proyectos."""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_project(self, project_name: str, description: str = "", template: str = "basico") -> bool:
        """Crea un nuevo proyecto con un template de sprints."""
        index = self._load_index()
        
        # Verificar si el proyecto ya existe
        if any(p.get("name") == project_name for p in index["projects"]):
            return False
        
        # Crear carpeta del proyecto
        project_dir = self.base_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Obtener template
        template_data = get_template(template)
        if not template_data:
            template_data = get_template("basico")
        
        # Crear archivo de información del proyecto
        project_info = {
            "name": project_name,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "scrum_file": str(project_dir / "scrum_board.json"),
            "template": template,
        }
        
        # Crear archivo scrum_board.json con sprints del template
        scrum_file = project_dir / "scrum_board.json"
        sprints_data = {
            "sprints": template_data.get("sprints", [])
        }
        
        with open(scrum_file, "w", encoding="utf-8") as f:
            json.dump(sprints_data, f, ensure_ascii=False, indent=2)
        
        # Agregar a índice
        index["projects"].append(project_info)
        self._save_index(index)
        
        return True

    def delete_project(self, project_name: str) -> bool:
        """Elimina un proyecto completo."""
        index = self._load_index()
        
        # Verificar si existe
        project_info = next((p for p in index["projects"] if p.get("name") == project_name), None)
        if not project_info:
            return False
        
        # Eliminar carpeta del proyecto
        project_dir = self.base_dir / project_name
        if project_dir.exists():
            shutil.rmtree(project_dir)
        
        # Actualizar índice
        index["projects"] = [p for p in index["projects"] if p.get("name") != project_name]
        if index["last_opened"] == project_name:
            index["last_opened"] = None
        self._save_index(index)
        
        return True

    def get_all_projects(self) -> list[dict[str, Any]]:
        """Retorna la lista de todos los proyectos."""
        index = self._load_index()
        return index.get("projects", [])

    def get_project(self, project_name: str) -> dict[str, Any] | None:
        """Retorna la información de un proyecto específico."""
        projects = self.get_all_projects()
        return next((p for p in projects if p.get("name") == project_name), None)

    def get_project_scrum_path(self, project_name: str) -> Path | None:
        """Retorna la ruta al archivo scrum_board.json del proyecto."""
        project = self.get_project(project_name)
        if project:
            return Path(project.get("scrum_file", ""))
        return None

    def set_last_opened(self, project_name: str) -> None:
        """Marca un proyecto como el últimamente abierto."""
        index = self._load_index()
        index["last_opened"] = project_name
        self._save_index(index)

    def get_last_opened(self) -> str | None:
        """Retorna el nombre del proyecto abierto recientemente."""
        index = self._load_index()
        last_opened = index.get("last_opened")
        
        # Verificar que el proyecto aún existe
        if last_opened:
            if self.get_project(last_opened):
                return last_opened
        
        return None

    def update_project_info(self, project_name: str, updates: dict[str, Any]) -> bool:
        """Actualiza la información de un proyecto."""
        index = self._load_index()
        
        for project in index["projects"]:
            if project.get("name") == project_name:
                project.update(updates)
                project["last_modified"] = datetime.now().isoformat()
                self._save_index(index)
                return True
        
        return False
