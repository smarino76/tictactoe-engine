# Proyecto: Tic-Tac-Toe Engine
# Autor: Santiago Marino
# Email: santiago.mmarino@gmail.com
# Año de desarrollo: 2026

import os

import joblib
from agent_ai import encode_state_action, get_available_actions
from tictactoe_engine import PlayerAgent


class ExpertAIAgent(PlayerAgent):
    def __init__(self, name="AI Player 1", model_path=None):
        """Inicializa el agente experto y carga el modelo entrenado si existe."""
        self.player_name = name
        self.model_path = model_path or f"{name}_model.pkl"
        self.model = None
        self.marker = None

        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)

    def act(self, state):
        """Elige la jugada disponible con mayor valor estimado por el modelo."""
        self.state = state
        available_actions = get_available_actions(state)

        if not available_actions:
            return None

        if self.marker is None:
            raise RuntimeError("El experto aun no tiene un marcador asignado.")

        if self.model is None:
            raise FileNotFoundError(
                f"No existe el modelo entrenado: {self.model_path}. "
                "Ejecuta train.py antes de usar el agente experto."
            )

        candidate_states = []
        for action in available_actions:
            candidate_states.append(encode_state_action(state, self.marker, action))

        predictions = self.model.predict(candidate_states)
        best_index = max(range(len(available_actions)), key=predictions.__getitem__)
        return available_actions[best_index]

    def event(self, message):
        """Acepta eventos del motor; el agente experto no necesita procesarlos."""
        pass