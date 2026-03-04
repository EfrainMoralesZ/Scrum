from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Any

import customtkinter as ctk
from Scrum import ScrumService


class ScrumView:
    """Interfaz gráfica moderna para visualizar y gestionar la tabla de Scrum."""

    def __init__(
        self,
        parent: ctk.CTk | ctk.CTkFrame,
        scrum_service: ScrumService,
        style: dict[str, str],
    ) -> None:
        self.parent = parent
        self.scrum_service = scrum_service
        self.style = style
        self.current_sprint = None
        self.tarea_cards: dict[int, dict[str, Any]] = {}
        self.bg_color = self.style.get("fondo", "#F8F9FA")
        self.surface_color = self.style.get("surface", "#FFFFFF")
        self.text_color = self.style.get("texto_oscuro", "#282828")
        self.border_color = self.style.get("borde", "#E0E0E0")
        self.grouped_mode = self.scrum_service.get_grouped_mode()  # Cargar estado persistido
        
        # Variables para las fuentes
        self.font_title = ("Inter", 22, "bold")
        self.font_subtitle = ("Inter", 16, "bold")
        self.font_label = ("Inter", 13)
        self.font_small = ("Inter", 11)

        self._create_widgets()
        self._load_sprints()

    def _create_widgets(self) -> None:
        """Crea los widgets principales de la vista con diseño moderno."""
        # Marco principal con scrolling
        main_frame = ctk.CTkFrame(self.parent, fg_color=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Marco superior (Título + Controles)
        header_frame = ctk.CTkFrame(main_frame, fg_color=self.bg_color)
        header_frame.pack(fill="x", pady=(0, 20))

        # Título
        title = ctk.CTkLabel(
            header_frame,
            text="🎯 Board de Scrum",
            font=self.font_title,
            text_color=self.text_color,
        )
        title.pack(anchor="w")

        # Marco de fechas del proyecto
        dates_frame = ctk.CTkFrame(header_frame, fg_color=self.surface_color, corner_radius=8)
        dates_frame.pack(fill="x", pady=(10, 15), padx=0)
        
        self.dates_label = ctk.CTkLabel(
            dates_frame,
            text="",
            font=self.font_small,
            text_color="#666666",
            justify="left",
        )
        self.dates_label.pack(anchor="w", padx=12, pady=8)

        # Marco de controles
        control_frame = ctk.CTkFrame(header_frame, fg_color=self.bg_color)
        control_frame.pack(fill="x", pady=(15, 0))

        # Selector de Sprint
        sprint_label = ctk.CTkLabel(
            control_frame,
            text="Sprint:",
            font=self.font_label,
            text_color=self.text_color,
        )
        sprint_label.pack(side="left", padx=(0, 10))

        self.sprint_var = tk.StringVar()
        self.sprint_combo = ctk.CTkComboBox(
            control_frame,
            variable=self.sprint_var,
            command=self._on_sprint_selected,
            width=180,
            font=self.font_label,
        )
        self.sprint_combo.pack(side="left", padx=(0, 30))

        # Botón para agregar tarea
        add_btn = ctk.CTkButton(
            control_frame,
            text="➕ Nueva Tarea",
            command=self._add_tarea_dialog,
            fg_color=self.style.get("btn_primario_bg", "#ECD925"),
            text_color=self.style.get("btn_primario_fg", self.text_color),
            hover_color=self.style.get("btn_primario_border", "#D4AF37"),
            font=self.font_label,
            height=35,
            border_width=2,
            border_color=self.style.get("btn_primario_border", "#D4B81D"),
        )
        add_btn.pack(side="left", padx=(0, 10))

        # Botón para actualizar vista
        refresh_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Actualizar",
            command=self._load_sprints,
            fg_color=self.style.get("btn_refresh_bg", "#F0F0F0"),
            text_color=self.style.get("btn_refresh_fg", "#666666"),
            hover_color=self.style.get("btn_refresh_bg", "#E0E0E0"),
            font=self.font_label,
            height=35,
            width=120,
            border_width=1,
            border_color=self.style.get("btn_refresh_border", "#D0D0D0"),
        )
        refresh_btn.pack(side="left")

        # Botón para agrupar/desagrupar tareas
        self.group_btn = ctk.CTkButton(
            control_frame,
            text="🔗 Agrupar por Duración",
            command=self._toggle_group_mode,
            fg_color=self.style.get("btn_group_bg", "#E8F4FD"),
            text_color=self.style.get("btn_group_fg", "#5B8DB8"),
            hover_color=self.style.get("btn_group_bg", "#D1E7F8"),
            font=self.font_label,
            height=35,
            width=200,
            border_width=1,
            border_color=self.style.get("btn_group_border", "#B8D4E8"),
        )
        self.group_btn.pack(side="left", padx=(15, 0))

        # Marco para resumen del sprint
        self.summary_frame = ctk.CTkFrame(main_frame, fg_color=self.bg_color, corner_radius=8)
        self.summary_frame.pack(fill="x", pady=(0, 20))

        self.summary_label = ctk.CTkLabel(
            self.summary_frame,
            text="",
            font=self.font_label,
            text_color=self.text_color,
            justify="left",
        )
        self.summary_label.pack(anchor="w", padx=15, pady=12)

        # Marco para las tareas (con scroll)
        tareas_header = ctk.CTkLabel(
            main_frame,
            text="Tareas del Sprint",
            font=self.font_subtitle,
            text_color=self.text_color,
        )
        tareas_header.pack(anchor="w", pady=(0, 15))

        # Contenedor scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            fg_color=self.bg_color,
            label_text="",
        )
        self.scroll_frame.pack(fill="both", expand=True)

    def _get_color_estado(self, estado: str) -> str:
        """Retorna el color según el estado de la tarea."""
        colors = {
            "Completado": self.style.get("exito", "#008D53"),
            "En Progreso": "#FF9500",
            "No Iniciado": "#CCCCCC",
        }
        return colors.get(estado, "#CCCCCC")

    def _get_icon_estado(self, estado: str) -> str:
        """Retorna el icono según el estado."""
        icons = {
            "Completado": "✓",
            "En Progreso": "⟳",
            "No Iniciado": "○",
        }
        return icons.get(estado, "○")

    def _load_sprints(self) -> None:
        """Carga los sprints en el combobox."""
        sprints = self.scrum_service.get_all_sprints()
        sprint_ids = [s.get("id", "") for s in sprints]
        self.sprint_combo.configure(values=sprint_ids)
        
        # Actualizar fechas del proyecto
        self._update_project_dates()
        
        if sprint_ids:
            selected = self.current_sprint if self.current_sprint in sprint_ids else sprint_ids[0]
            self.sprint_combo.set(selected)
            self._on_sprint_selected(selected)

    def _on_sprint_selected(self, value: str | None) -> None:
        """Maneja la selección de un sprint."""
        sprint_id = value or self.sprint_var.get()
        if sprint_id:
            self.current_sprint = sprint_id
            self._load_tareas(sprint_id)

    def _update_summary(self, summary: dict[str, Any]) -> None:
        """Actualiza el label de resumen del sprint."""
        total = summary.get("total_tareas", 0)
        completadas = summary.get("tareas_completadas", 0)
        en_progreso = summary.get("tareas_en_progreso", 0)
        tiempo = summary.get("tiempo_estimado_total", 0)
        porcentaje = summary.get("porcentaje_completado", 0)
        
        # Calcular total de días del proyecto
        tiempo_total_proyecto = self._calculate_project_total_days()

        summary_text = (
            f"📊 Sprint: {total} tareas | "
            f"✓ Completadas: {completadas} | "
            f"⟳ En Progreso: {en_progreso} | "
            f"⏱ Sprint: {tiempo}d | "
            f"🎯 Proyecto Total: {tiempo_total_proyecto}d | "
            f"📈 Progreso: {porcentaje:.0f}%"
        )
        self.summary_label.configure(text=summary_text)

    def _create_tarea_card(self, idx: int, tarea: dict[str, Any], parent_frame=None) -> None:
        """Crea una tarjeta visual para una tarea."""
        if parent_frame is None:
            parent_frame = self.scroll_frame

        titulo = tarea.get("titulo", "Sin título")
        descripcion = tarea.get("descripcion", "")
        dias = tarea.get("tiempo_estimado_dias", 0)
        estado = tarea.get("estado", "No Iniciado")
        asignado = tarea.get("asignado_a", "Sin asignar")

        # Marco principal de la tarjeta
        card_frame = ctk.CTkFrame(
            parent_frame,
            fg_color=self.surface_color,
            border_width=1,
            border_color=self.border_color,
            corner_radius=10,
        )
        card_frame.pack(fill="x", padx=0, pady=10)

        # Encabezado de la tarjeta
        header_frame = ctk.CTkFrame(card_frame, fg_color=self.surface_color)
        header_frame.pack(fill="x", padx=15, pady=(12, 0))

        # Título + Estado
        title_state_frame = ctk.CTkFrame(header_frame, fg_color=self.surface_color)
        title_state_frame.pack(fill="x", expand=True)

        title_label = ctk.CTkLabel(
            title_state_frame,
            text=titulo,
            font=self.font_subtitle,
            text_color=self.text_color,
            anchor="w",
        )
        title_label.pack(side="left", expand=True, fill="x")

        # Badge de estado
        estado_color = self._get_color_estado(estado)
        estado_icon = self._get_icon_estado(estado)
        estado_badge = ctk.CTkLabel(
            title_state_frame,
            text=f"{estado_icon} {estado}",
            font=("Inter", 10, "bold"),
            text_color="white",
            fg_color=estado_color,
            corner_radius=6,
            padx=10,
            pady=4,
        )
        estado_badge.pack(side="right", padx=(10, 0))

        # Descripción
        if descripcion:
            desc_label = ctk.CTkLabel(
                card_frame,
                text=descripcion,
                font=self.font_small,
                text_color="#666666",
                anchor="w",
                wraplength=600,
                justify="left",
            )
            desc_label.pack(fill="x", padx=15, pady=(8, 0), anchor="w")

        # Footer con información
        footer_frame = ctk.CTkFrame(card_frame, fg_color=self.surface_color)
        footer_frame.pack(fill="x", padx=15, pady=(10, 0))

        # Información
        info_text = f"⏱ {dias}d  |  👤 {asignado}"
        info_label = ctk.CTkLabel(
            footer_frame,
            text=info_text,
            font=self.font_small,
            text_color="#999999",
        )
        info_label.pack(side="left")

        # Botones de acción
        action_frame = ctk.CTkFrame(footer_frame, fg_color=self.surface_color)
        action_frame.pack(side="right")

        edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️ Editar",
            command=lambda i=idx: self._edit_tarea(i),
            fg_color=self.style.get("btn_editar_bg", "#E8F4FD"),
            text_color=self.style.get("btn_editar_fg", "#5B8DB8"),
            hover_color=self.style.get("btn_editar_bg", "#D1E7F8"),
            font=self.font_small,
            height=28,
            width=80,
            border_width=1,
            border_color=self.style.get("btn_editar_border", "#B8D4E8"),
        )
        edit_btn.pack(side="left", padx=(0, 5))

        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Borrar",
            command=lambda i=idx: self._delete_tarea(i),
            fg_color=self.style.get("btn_borrar_bg", "#FFE5E5"),
            text_color=self.style.get("btn_borrar_fg", "#C85A54"),
            hover_color=self.style.get("btn_borrar_bg", "#FFD1D1"),
            font=self.font_small,
            height=28,
            width=80,
            border_width=1,
            border_color=self.style.get("btn_borrar_border", "#F5B8B8"),
        )
        delete_btn.pack(side="left", padx=(0, 0))

        # Espaciado extra
        footer_frame.pack(fill="x", padx=15, pady=(0, 12))

        self.tarea_cards[idx] = card_frame

    def _add_tarea_dialog(self) -> None:
        """Abre un diálogo mejorado para agregar una nueva tarea."""
        if not self.current_sprint:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un sprint primero.")
            return

        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel()
        dialog.title("➕ Nueva Tarea - Board de Scrum")
        dialog.geometry("650x620")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.bg_color)

        # Centrar la ventana
        dialog.transient(self.parent)
        dialog.grab_set()

        # Marco principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color=self.surface_color)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Encabezado con título
        title = ctk.CTkLabel(
            main_frame,
            text="✨ Agregar Nueva Tarea",
            font=self.font_subtitle,
            text_color=self.text_color,
        )
        title.pack(anchor="w", pady=(0, 25))

        # Marco de contenido principal
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.surface_color, corner_radius=12, border_width=1, border_color=self.border_color)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título de tarea
        titulo_label = ctk.CTkLabel(
            content_frame,
            text="📌 Título de la tarea *",
            font=self.font_label,
            text_color=self.text_color,
        )
        titulo_label.pack(anchor="w", padx=18, pady=(15, 8))
        titulo_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Ej: Crear interfaz de usuario",
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        titulo_entry.pack(fill="x", padx=18, pady=(0, 15))

        # Descripción
        desc_label = ctk.CTkLabel(
            content_frame,
            text="📝 Descripción",
            font=self.font_label,
            text_color=self.text_color,
        )
        desc_label.pack(anchor="w", padx=18, pady=(0, 8))
        desc_text = ctk.CTkTextbox(content_frame, height=100, font=self.font_small, border_width=1, border_color=self.border_color)
        desc_text.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        # Frame para Días y Estado
        row_frame = ctk.CTkFrame(content_frame, fg_color=self.surface_color)
        row_frame.pack(fill="x", padx=18, pady=(0, 15))

        dias_frame = ctk.CTkFrame(row_frame, fg_color=self.surface_color)
        dias_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        dias_label = ctk.CTkLabel(
            dias_frame,
            text="⏱ Días Estimados",
            font=self.font_label,
            text_color=self.text_color,
        )
        dias_label.pack(anchor="w", pady=(0, 8))
        dias_entry = ctk.CTkEntry(dias_frame, placeholder_text="1", font=self.font_label, height=40, border_width=1, border_color=self.border_color)
        dias_entry.insert(0, "1")
        dias_entry.pack(fill="x")

        # Estado
        estado_frame = ctk.CTkFrame(row_frame, fg_color=self.surface_color)
        estado_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        estado_label = ctk.CTkLabel(
            estado_frame,
            text="🎯 Estado",
            font=self.font_label,
            text_color=self.text_color,
        )
        estado_label.pack(anchor="w", pady=(0, 8))
        estado_var = tk.StringVar(value="No Iniciado")
        estado_combo = ctk.CTkComboBox(
            estado_frame,
            variable=estado_var,
            values=["No Iniciado", "En Progreso", "Completado"],
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        estado_combo.pack(fill="x")

        # Asignado a
        asig_label = ctk.CTkLabel(
            content_frame,
            text="👤 Asignado a",
            font=self.font_label,
            text_color=self.text_color,
        )
        asig_label.pack(anchor="w", padx=18, pady=(0, 8))
        asig_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Nombre o equipo responsable",
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        asig_entry.pack(fill="x", padx=18, pady=(0, 15))

        def save_tarea() -> None:
            titulo = titulo_entry.get().strip()
            descripcion = desc_text.get("1.0", "end").strip()
            
            if not titulo:
                messagebox.showwarning("Validación", "El título es obligatorio.")
                return

            try:
                dias = int(dias_entry.get())
            except ValueError:
                messagebox.showerror("Validación", "Los días deben ser un número válido.")
                return

            tarea = {
                "titulo": titulo,
                "descripcion": descripcion,
                "tiempo_estimado_dias": dias,
                "estado": estado_var.get(),
                "asignado_a": asig_entry.get().strip(),
            }

            if self.scrum_service.add_tarea(self.current_sprint, tarea):
                messagebox.showinfo("Éxito", "¡Tarea agregada correctamente!")
                self._load_tareas(self.current_sprint)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar la tarea.")

        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color=self.surface_color)
        btn_frame.pack(fill="x", pady=(0, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Tarea",
            command=save_tarea,
            fg_color=self.style.get("btn_primario_bg", "#ECD925"),
            text_color=self.style.get("btn_primario_fg", self.text_color),
            hover_color=self.style.get("btn_primario_border", "#D4AF37"),
            font=self.font_label,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color=self.style.get("btn_primario_border", "#D4B81D"),
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

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

    def _edit_tarea(self, tarea_index: int) -> None:
        """Abre un diálogo para editar una tarea."""
        if not self.current_sprint:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un sprint primero.")
            return

        sprint = self.scrum_service.get_sprint(self.current_sprint)
        if not sprint or tarea_index >= len(sprint.get("tareas", [])):
            messagebox.showerror("Error", "Tarea no encontrada.")
            return

        tarea = sprint["tareas"][tarea_index]

        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel()
        dialog.title("✏️ Editar Tarea - Board de Scrum")
        dialog.geometry("650x620")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.bg_color)

        dialog.transient(self.parent)
        dialog.grab_set()

        # Marco principal con scroll
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color=self.surface_color)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="✏️ Editar Tarea",
            font=self.font_subtitle,
            text_color=self.text_color,
        )
        title.pack(anchor="w", pady=(0, 25))

        # Marco de contenido principal
        content_frame = ctk.CTkFrame(main_frame, fg_color=self.surface_color, corner_radius=12, border_width=1, border_color=self.border_color)
        content_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Título de tarea
        titulo_label = ctk.CTkLabel(
            content_frame,
            text="📌 Título de la tarea",
            font=self.font_label,
            text_color=self.text_color,
        )
        titulo_label.pack(anchor="w", padx=18, pady=(15, 8))
        titulo_entry = ctk.CTkEntry(content_frame, font=self.font_label, height=40, border_width=1, border_color=self.border_color)
        titulo_entry.insert(0, tarea.get("titulo", ""))
        titulo_entry.pack(fill="x", padx=18, pady=(0, 15))

        # Descripción
        desc_label = ctk.CTkLabel(
            content_frame,
            text="📝 Descripción",
            font=self.font_label,
            text_color=self.text_color,
        )
        desc_label.pack(anchor="w", padx=18, pady=(0, 8))
        desc_text = ctk.CTkTextbox(content_frame, height=100, font=self.font_small, border_width=1, border_color=self.border_color)
        desc_text.insert("1.0", tarea.get("descripcion", ""))
        desc_text.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        # Frame para Días y Estado
        row_frame = ctk.CTkFrame(content_frame, fg_color=self.surface_color)
        row_frame.pack(fill="x", padx=18, pady=(0, 15))

        dias_frame = ctk.CTkFrame(row_frame, fg_color=self.surface_color)
        dias_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        dias_label = ctk.CTkLabel(
            dias_frame,
            text="⏱ Días Estimados",
            font=self.font_label,
            text_color=self.text_color,
        )
        dias_label.pack(anchor="w", pady=(0, 8))
        dias_entry = ctk.CTkEntry(dias_frame, font=self.font_label, height=40, border_width=1, border_color=self.border_color)
        dias_entry.insert(0, str(tarea.get("tiempo_estimado_dias", 0)))
        dias_entry.pack(fill="x")

        # Estado
        estado_frame = ctk.CTkFrame(row_frame, fg_color=self.surface_color)
        estado_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        estado_label = ctk.CTkLabel(
            estado_frame,
            text="🎯 Estado",
            font=self.font_label,
            text_color=self.text_color,
        )
        estado_label.pack(anchor="w", pady=(0, 8))
        estado_var = tk.StringVar(value=tarea.get("estado", "No Iniciado"))
        estado_combo = ctk.CTkComboBox(
            estado_frame,
            variable=estado_var,
            values=["No Iniciado", "En Progreso", "Completado"],
            font=self.font_label,
            height=40,
            border_width=1,
            border_color=self.border_color,
        )
        estado_combo.pack(fill="x")

        # Asignado a
        asig_label = ctk.CTkLabel(
            content_frame,
            text="👤 Asignado a",
            font=self.font_label,
            text_color=self.text_color,
        )
        asig_label.pack(anchor="w", padx=18, pady=(0, 8))
        asig_entry = ctk.CTkEntry(content_frame, font=self.font_label, height=40, border_width=1, border_color=self.border_color)
        asig_entry.insert(0, tarea.get("asignado_a", ""))
        asig_entry.pack(fill="x", padx=18, pady=(0, 15))

        def save_changes() -> None:
            titulo = titulo_entry.get().strip()
            if not titulo:
                messagebox.showwarning("Validación", "El título es obligatorio.")
                return

            try:
                dias = int(dias_entry.get())
            except ValueError:
                messagebox.showerror("Validación", "Los días deben ser un número válido.")
                return

            updates = {
                "titulo": titulo,
                "descripcion": desc_text.get("1.0", "end").strip(),
                "tiempo_estimado_dias": dias,
                "estado": estado_var.get(),
                "asignado_a": asig_entry.get().strip(),
            }

            if self.scrum_service.update_tarea(self.current_sprint, tarea_index, updates):
                messagebox.showinfo("Éxito", "¡Tarea actualizada correctamente!")
                self._load_tareas(self.current_sprint)
                dialog.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la tarea.")
        
        # Botones
        btn_frame = ctk.CTkFrame(main_frame, fg_color=self.surface_color)
        btn_frame.pack(fill="x", pady=(0, 0))

        save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Cambios",
            command=save_changes,
            fg_color=self.style.get("btn_primario_bg", "#ECD925"),
            text_color=self.style.get("btn_primario_fg", self.text_color),
            hover_color=self.style.get("btn_primario_border", "#D4AF37"),
            font=self.font_label,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color=self.style.get("btn_primario_border", "#D4B81D"),
        )
        save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

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

    def _delete_tarea(self, tarea_index: int) -> None:
        """Elimina una tarea después de confirmación."""
        if messagebox.askyesno("Confirmar eliminación", "¿Deseas eliminar esta tarea?"):
            if self.scrum_service.delete_tarea(self.current_sprint, tarea_index):
                messagebox.showinfo("Éxito", "¡Tarea eliminada correctamente!")
                self._load_tareas(self.current_sprint)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea.")
    def _calculate_project_total_days(self) -> int:
        """Calcula el total de días estimados para todo el proyecto."""
        sprints = self.scrum_service.get_all_sprints()
        total_dias = 0
        
        if self.grouped_mode:
            # En modo agrupado, contar días únicos (tareas paralelas)
            dias_unicos = set()
            for sprint in sprints:
                tareas = sprint.get("tareas", [])
                for tarea in tareas:
                    dias = tarea.get("tiempo_estimado_dias", 0)
                    dias_unicos.add(dias)
            total_dias = sum(dias_unicos)
        else:
            # En modo normal, sumar todos los días (tareas secuenciales)
            for sprint in sprints:
                tareas = sprint.get("tareas", [])
                for tarea in tareas:
                    total_dias += tarea.get("tiempo_estimado_dias", 0)
        
        return total_dias

    def _toggle_group_mode(self) -> None:
        """Alterna el modo de agrupación de tareas."""
        self.grouped_mode = not self.grouped_mode
        self.scrum_service.set_grouped_mode(self.grouped_mode)  # Guardar cambio
        
        if self.grouped_mode:
            self.group_btn.configure(
                text="🔓 Desagrupar por Duración",
                fg_color=self.style.get("btn_group_active_bg", "#FFF4E5"),
                text_color=self.style.get("btn_group_active_fg", "#D87A16"),
                hover_color=self.style.get("btn_group_active_bg", "#FFE8CC"),
                border_color=self.style.get("btn_group_active_border", "#FFBB7A")
            )
        else:
            self.group_btn.configure(
                text="🔗 Agrupar por Duración",
                fg_color=self.style.get("btn_group_bg", "#E8F4FD"),
                text_color=self.style.get("btn_group_fg", "#5B8DB8"),
                hover_color=self.style.get("btn_group_bg", "#D1E7F8"),
                border_color=self.style.get("btn_group_border", "#B8D4E8")
            )
        
        # Recargar las tareas con el nuevo modo
        if self.current_sprint:
            self._load_tareas(self.current_sprint)

    def _load_tareas(self, sprint_id: str) -> None:
        """Carga las tareas del sprint en formato de cards (con opción de agrupación)."""
        # Limpiar el frame anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.tarea_cards.clear()

        sprint = self.scrum_service.get_sprint(sprint_id)
        if not sprint:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No hay tareas en este sprint",
                font=self.font_label,
                text_color="#999999",
            )
            empty_label.pack(pady=20)
            return

        tareas = sprint.get("tareas", [])
        
        if not tareas:
            empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No hay tareas en este sprint",
                font=self.font_label,
                text_color="#999999",
            )
            empty_label.pack(pady=20)
        else:
            if self.grouped_mode:
                # Agrupar tareas por duración
                grouped_tareas = self._group_tareas_by_duration(tareas)
                for dias, tareas_grupo in grouped_tareas:
                    self._create_duration_group(dias, tareas_grupo)
            else:
                # Mostrar tareas sin agrupar
                for idx, tarea in enumerate(tareas):
                    self._create_tarea_card(idx, tarea)

        # Actualizar resumen
        summary = self.scrum_service.get_sprint_summary(sprint_id)
        self._update_summary(summary)

    def _group_tareas_by_duration(self, tareas: list[dict[str, Any]]) -> list[tuple[int, list[tuple[int, dict[str, Any]]]]]:
        """Agrupa tareas por su duración en días."""
        grupos: dict[int, list[tuple[int, dict[str, Any]]]] = {}
        
        for idx, tarea in enumerate(tareas):
            dias = tarea.get("tiempo_estimado_dias", 0)
            if dias not in grupos:
                grupos[dias] = []
            grupos[dias].append((idx, tarea))
        
        # Retornar grupos ordenados por duración
        return sorted(grupos.items(), key=lambda x: x[0])

    def _create_duration_group(self, dias: int, tareas_grupo: list[tuple[int, dict[str, Any]]]) -> None:
        """Crea un grupo visual de tareas con la misma duración."""
        # Marco del grupo
        group_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=self.surface_color,
            corner_radius=8,
            border_width=1,
            border_color=self.border_color,
        )
        group_frame.pack(fill="x", pady=12)

        # Encabezado del grupo
        header_frame = ctk.CTkFrame(group_frame, fg_color=self.surface_color)
        header_frame.pack(fill="x", padx=15, pady=(12, 0))

        group_title = ctk.CTkLabel(
            header_frame,
            text=f"⏱ {dias} día{'s' if dias != 1 else ''}",
            font=("Inter", 14, "bold"),
            text_color=self.style.get("primario", "#ECD925"),
        )
        group_title.pack(side="left")

        count_label = ctk.CTkLabel(
            header_frame,
            text=f"({len(tareas_grupo)} tarea{'s' if len(tareas_grupo) != 1 else ''})",
            font=self.font_small,
            text_color="#999999",
        )
        count_label.pack(side="left", padx=(10, 0))

        # Separador
        separator = ctk.CTkFrame(group_frame, fg_color=self.border_color, height=1)
        separator.pack(fill="x", padx=15, pady=(8, 0))

        # Contenedor de tareas del grupo
        tareas_frame = ctk.CTkFrame(group_frame, fg_color=self.surface_color)
        tareas_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Mostrar tareas del grupo
        for idx, tarea in tareas_grupo:
            self._create_tarea_card(idx, tarea, parent_frame=tareas_frame)

    def _update_project_dates(self) -> None:
        """Actualiza la información de fechas del proyecto."""
        from datetime import datetime, timedelta
        
        try:
            dates_info = self.scrum_service.get_project_dates()
            start_date = dates_info["start_date"]
            estimated_end = dates_info["estimated_end_date"]
            total_days = dates_info["total_estimated_days"]
            
            # Calcular día actual del proyecto
            today = datetime.now()
            days_elapsed = (today - start_date).days
            
            # Formato de fechas
            start_str = start_date.strftime("%d/%m/%Y")
            end_str = estimated_end.strftime("%d/%m/%Y")
            
            # Texto de información
            dates_text = f"📅 Inicio: {start_str}  |  Fin estimado: {end_str}  |  Total: {total_days} días  |  Día actual: {max(0, days_elapsed + 1)}/{total_days}"
            
            self.dates_label.configure(text=dates_text)
        except Exception:
            # Si hay error, no mostrar fechas
            self.dates_label.configure(text="")