"""Templates de proyectos Scrum con sprints y tareas predefinidas."""

from typing import Any

TEMPLATES = {
    "basico": {
        "name": "Proyecto Básico",
        "description": "Estructura básica de 3 sprints para empezar",
        "sprints": [
            {
                "id": "Sprint 1 - Iniciación",
                "tareas": [
                    {
                        "titulo": "Planificación del proyecto",
                        "descripcion": "Definir objetivos, alcance y recursos",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Configuración del entorno",
                        "descripcion": "Preparar herramientas y arquitectura base",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
            {
                "id": "Sprint 2 - Desarrollo",
                "tareas": [
                    {
                        "titulo": "Implementar funcionalidades core",
                        "descripcion": "Desarrollar características principales del proyecto",
                        "tiempo_estimado_dias": 5,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Crear pruebas unitarias",
                        "descripcion": "Implementar tests para funcionalidades",
                        "tiempo_estimado_dias": 3,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
            {
                "id": "Sprint 3 - Cierre",
                "tareas": [
                    {
                        "titulo": "Testing y QA",
                        "descripcion": "Verificar calidad y resolver bugs",
                        "tiempo_estimado_dias": 3,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Documentación",
                        "descripcion": "Crear documentación del proyecto",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
        ]
    },
    "aplicacion_web": {
        "name": "Aplicación Web",
        "description": "Template para desarrollo de aplicación web",
        "sprints": [
            {
                "id": "Sprint 1 - Configuración Base",
                "tareas": [
                    {
                        "titulo": "Crear estructura del proyecto",
                        "descripcion": "Configurar repositorio y estructura base",
                        "tiempo_estimado_dias": 1,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Diseñar base de datos",
                        "descripcion": "Crear esquema DB y modelos.",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Configurar backend inicial",
                        "descripcion": "Setup de API y autenticación",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
            {
                "id": "Sprint 2 - Desarrollo Frontend",
                "tareas": [
                    {
                        "titulo": "Crear página de inicio",
                        "descripcion": "Diseño e implementación de inicio",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Implementar formularios",
                        "descripcion": "Crear formularios interactivos",
                        "tiempo_estimado_dias": 3,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Componentes reutilizables",
                        "descripcion": "Crear librería de componentes",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
            {
                "id": "Sprint 3 - Desarrollo Backend",
                "tareas": [
                    {
                        "titulo": "Endpoints principales",
                        "descripcion": "Implementar APIs REST",
                        "tiempo_estimado_dias": 3,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Validaciones y seguridad",
                        "descripcion": "Agregar validaciones y protecciones",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
            {
                "id": "Sprint 4 - Testing y Deploy",
                "tareas": [
                    {
                        "titulo": "Testing integración",
                        "descripcion": "Pruebas end-to-end",
                        "tiempo_estimado_dias": 2,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                    {
                        "titulo": "Despliegue a producción",
                        "descripcion": "Deploy de la aplicación",
                        "tiempo_estimado_dias": 1,
                        "estado": "No Iniciado",
                        "asignado_a": "",
                        "fecha_inicio": None,
                        "fecha_fin": None,
                    },
                ]
            },
        ]
    }
}


def get_template(template_name: str) -> dict[str, Any] | None:
    """Obtiene un template por nombre."""
    return TEMPLATES.get(template_name)


def get_template_names() -> list[str]:
    """Retorna lista de nombres de templates disponibles."""
    return list(TEMPLATES.keys())


def get_template_descriptions() -> dict[str, str]:
    """Retorna descripción de cada template."""
    return {
        name: template.get("description", "")
        for name, template in TEMPLATES.items()
    }
