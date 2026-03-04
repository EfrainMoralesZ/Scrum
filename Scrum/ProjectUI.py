"""Interfaz de gestión de proyectos Scrum."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import Any, Callable

import customtkinter as ctk
from ProjectManager import ProjectManager
from ProjectTemplates import get_template_names, get_template_descriptions


class ProjectSelectionView:
    """Interfaz para seleccionar o crear proyectos Scrum."""

    def __init__(
        self,
        parent: ctk.CTk,
        style: dict[str, str],
        on_project_selected: Callable[[str], None],
        on_theme_change: Callable[[], None] = None,
    ) -> None:
        self.parent = parent
        self.style = style
        self.on_project_selected = on_project_selected
        self.on_theme_change = on_theme_change
        self.project_manager = ProjectManager(base_dir="projects")
        
        # Colores
        self.bg_color = self.style.get("fondo", "#F8F9FA")
        self.surface_color = self.style.get("surface", "#FFFFFF")
        self.text_color = self.style.get("texto_oscuro", "#282828")
        self.border_color = self.style.get("borde", "#E0E0E0")
        self.primary_color = self.style.get("primario", "#ECD925")
        
        # Fuentes
        self.font_title = ("Inter", 24, "bold")
        self.font_subtitle = ("Inter", 16, "bold")
        self.font_label = ("Inter", 13)
        self.font_small = ("Inter", 11)

        self._create_widgets()
        self._load_projects()

    def _create_widgets(self) -> None:
        """Crea los widgets de la vista de proyectos."""
        # Marco principal con padding reducido
        main_frame = ctk.CTkFrame(self.parent, fg_color=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Encabezado
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 30))

        title = ctk.CTkLabel(
            header_frame,
            text="📁 Mis Proyectos Scrum",
            font=self.font_title,
            text_color=self.text_color,
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Gestiona y organiza tus proyectos de desarrollo",
            font=self.font_small,
            text_color="#999999",
        )
        subtitle.pack(anchor="w", pady=(8, 0))

        # Marco de controles
        control_frame = ctk.CTkFrame(main_frame, fg_color=self.bg_color)
        control_frame.pack(fill="x", pady=(0, 20))

        new_project_btn = ctk.CTkButton(
            control_frame,
            text="➕ Nuevo Proyecto",
            command=self._create_project_dialog,
            fg_color=self.style.get("btn_primario_bg", self.primary_color),
            text_color=self.style.get("btn_primario_fg", self.text_color),
            hover_color=self.style.get("btn_primario_border", "#D4AF37"),
            font=self.font_label,
            height=42,
            corner_radius=8,
            border_width=2,
            border_color=self.style.get("btn_primario_border", "#D4B81D"),
        )
        new_project_btn.pack(side="left", padx=(0, 15))
        
        # Botón de cambio de tema
        if self.on_theme_change:
            theme_btn = ctk.CTkButton(
                control_frame,
                text="🌙/☀️",
                command=self.on_theme_change,
                fg_color=self.style.get("btn_refresh_bg", "#F0F0F0"),
                font=("Inter", 14),
                height=42,
                width=60,
                border_width=1,
                border_color=self.style.get("btn_refresh_border", "#D0D0D0"),
            )
            theme_btn.pack(side="right")

        refresh_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Actualizar",
            command=self._load_projects,
            fg_color=self.style.get("btn_refresh_bg", "#F0F0F0"),
            text_color=self.style.get("btn_refresh_fg", "#666666"),
            hover_color=self.style.get("btn_refresh_bg", "#E0E0E0"),
            font=self.font_label,
            height=42,
            corner_radius=8,
            width=120,
            border_width=1,
            border_color=self.style.get("btn_refresh_border", "#D0D0D0"),
        )
        refresh_btn.pack(side="left")

        # Marco para proyectos
        self.projects_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=self.bg_color,
        )
        self.projects_frame.pack(fill="both", expand=True)

    def _load_projects(self) -> None:
        """Carga y muestra los proyectos."""
        # Limpiar frame
        for widget in self.projects_frame.winfo_children():
            widget.destroy()

        projects = self.project_manager.get_all_projects()

        if not projects:
            empty_label = ctk.CTkLabel(
                self.projects_frame,
                text="📭 No hay proyectos aún. ¡Crea uno nuevo para empezar!",
                font=self.font_label,
                text_color="#999999",
            )
            empty_label.pack(pady=40)
        else:
            for project in projects:
                self._create_project_card(project)

    def _create_project_card(self, project: dict[str, Any]) -> None:
        """Crea una tarjeta para un proyecto."""
        name = project.get("name", "Sin nombre")
        description = project.get("description", "")
        created = project.get("created_at", "")

        # Marco de la tarjeta
        card_frame = ctk.CTkFrame(
            self.projects_frame,
            fg_color=self.surface_color,
            border_width=1,
            border_color=self.border_color,
            corner_radius=10,
        )
        card_frame.pack(fill="x", pady=12)

        # Contenido principal
        content_frame = ctk.CTkFrame(card_frame, fg_color=self.surface_color)
        content_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Encabezado de tarjeta
        header_frame = ctk.CTkFrame(content_frame, fg_color=self.surface_color)
        header_frame.pack(fill="x", expand=True)

        name_label = ctk.CTkLabel(
            header_frame,
            text=f"📋 {name}",
            font=self.font_subtitle,
            text_color=self.text_color,
        )
        name_label.pack(side="left", expand=True, anchor="w")

        # Descripción
        if description:
            desc_label = ctk.CTkLabel(
                content_frame,
                text=description,
                font=self.font_small,
                text_color="#666666",
                wraplength=500,
                justify="left",
            )
            desc_label.pack(fill="x", anchor="w", pady=(8, 0))

        # Footer de tarjeta
        footer_frame = ctk.CTkFrame(content_frame, fg_color=self.surface_color)
        footer_frame.pack(fill="x", pady=(12, 0))

        created_label = ctk.CTkLabel(
            footer_frame,
            text=f"📅 {created[:10] if created else 'N/A'}",
            font=self.font_small,
            text_color="#999999",
        )
        created_label.pack(side="left")

        # Botones de acción
        button_frame = ctk.CTkFrame(footer_frame, fg_color=self.surface_color)
        button_frame.pack(side="right")

        open_btn = ctk.CTkButton(
            button_frame,
            text="🚀 Abrir",
            command=lambda n=name: self._open_project(n),
            fg_color=self.style.get("btn_editar_bg", "#E8F4FD"),
            text_color=self.style.get("btn_editar_fg", "#5B8DB8"),
            hover_color=self.style.get("btn_editar_bg", "#D1E7F8"),
            font=self.font_small,
            height=28,
            width=80,
            border_width=1,
            border_color=self.style.get("btn_editar_border", "#B8D4E8"),
        )
        open_btn.pack(side="left", padx=(0, 8))

        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Eliminar",
            command=lambda n=name: self._delete_project(n),
            fg_color=self.style.get("btn_borrar_bg", "#FFE5E5"),
            text_color=self.style.get("btn_borrar_fg", "#C85A54"),
            hover_color=self.style.get("btn_borrar_bg", "#FFD1D1"),
            font=self.font_small,
            height=32,
            width=90,
            border_width=1,
            border_color=self.style.get("btn_borrar_border", "#F5B8B8"),
        )
        delete_btn.pack(side="left")

    def _open_project(self, project_name: str) -> None:
        """Abre un proyecto."""
        self.project_manager.set_last_opened(project_name)
        self.on_project_selected(project_name)

    def _delete_project(self, project_name: str) -> None:
        """Elimina un proyecto con confirmación."""
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar el proyecto '{project_name}' permanentemente?",
        ):
            if self.project_manager.delete_project(project_name):
                messagebox.showinfo("Éxito", "Proyecto eliminado correctamente.")
                self._load_projects()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proyecto.")

    def _create_project_dialog(self) -> None:
        """Abre un diálogo para crear un nuevo proyecto con plantilla."""
        dialog = ctk.CTkToplevel()
        dialog.title("➕ Nuevo Proyecto")
        dialog.geometry("550x580")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.bg_color)

        dialog.transient(self.parent)
        dialog.grab_set()

        # Marco principal
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color=self.surface_color)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="✨ Crear Nuevo Proyecto",
            font=self.font_subtitle,
            text_color=self.text_color,
        )
        title.pack(anchor="w", pady=(0, 20))

        # Marco de contenido
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.surface_color, corner_radius=12, border_width=1, border_color=self.border_color)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Nombre del proyecto
        name_label = ctk.CTkLabel(
            content_frame,
            text="📌 Nombre del Proyecto *",
            font=self.font_label,
            text_color=self.text_color,
        )
        name_label.pack(anchor="w", padx=18, pady=(15, 8))

        name_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Ej: Mi Aplicación Web",
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        name_entry.pack(fill="x", padx=18, pady=(0, 15))

        # Descripción
        desc_label = ctk.CTkLabel(
            content_frame,
            text="📝 Descripción",
            font=self.font_label,
            text_color=self.text_color,
        )
        desc_label.pack(anchor="w", padx=18, pady=(0, 8))

        desc_text = ctk.CTkTextbox(
            content_frame,
            height=70,
            font=self.font_small,
            border_width=1,
            border_color=self.border_color,
        )
        desc_text.pack(fill="both", padx=18, pady=(0, 15))

        # Template selector
        template_label = ctk.CTkLabel(
            content_frame,
            text="🎯 Plantilla de Sprints",
            font=self.font_label,
            text_color=self.text_color,
        )
        template_label.pack(anchor="w", padx=18, pady=(0, 8))

        template_var = tk.StringVar(value="basico")
        template_names = get_template_names()
        template_descriptions = get_template_descriptions()

        template_combo = ctk.CTkComboBox(
            content_frame,
            variable=template_var,
            values=template_names,
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        template_combo.pack(fill="x", padx=18, pady=(0, 8))

        # Descripción del template seleccionado
        def update_template_desc(choice):
            desc = template_descriptions.get(choice, "")
            template_desc_label.configure(text=desc)

        template_combo.configure(command=update_template_desc)

        template_desc_label = ctk.CTkLabel(
            content_frame,
            text=template_descriptions.get("basico", ""),
            font=self.font_small,
            text_color="#666666",
            wraplength=400,
            justify="left",
        )
        template_desc_label.pack(anchor="w", padx=18, pady=(0, 15))

        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color=self.bg_color)
        btn_frame.pack(fill="x")

        def save_project():
            proj_name = name_entry.get().strip()
            proj_desc = desc_text.get("1.0", "end").strip()
            template = template_var.get()

            if not proj_name:
                messagebox.showwarning("Validación", "El nombre del proyecto es obligatorio.")
                return

            if self.project_manager.create_project(proj_name, proj_desc, template=template):
                messagebox.showinfo("Éxito", f"Proyecto '{proj_name}' creado correctamente.")
                self._load_projects()
                dialog.destroy()
                self._open_project(proj_name)
            else:
                messagebox.showerror("Error", f"El proyecto '{proj_name}' ya existe.")

        create_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Crear Proyecto",
            command=save_project,
            fg_color=self.style.get("btn_primario_bg", self.primary_color),
            text_color=self.style.get("btn_primario_fg", self.text_color),
            hover_color=self.style.get("btn_primario_border", "#D4AF37"),
            font=self.font_label,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color=self.style.get("btn_primario_border", "#D4B81D"),
        )
        create_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=dialog.destroy,
            fg_color="#E0E0E0",
            text_color="#282828",
            font=self.font_label,
            height=45,
            corner_radius=8,
        )
        cancel_btn.pack(side="left", fill="x", expand=True)
