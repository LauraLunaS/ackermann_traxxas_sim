"""Empacota os frames .obj/.mtl ja extraidos em modelos Gazebo (model.config + model.sdf)."""
import os
import shutil
import sys

MODELS_DIR = (
    '/home/lauraluna/ackermann_sim/src/ackermann-vehicle-gzsim-ros2/'
    'saye_description/models')

MODEL_SDF_TEMPLATE = """<?xml version="1.0" ?>
<sdf version="1.8">
  <model name="{nome}">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry>
          <mesh><uri>meshes/walk.obj</uri></mesh>
        </geometry>
      </visual>
    </link>
  </model>
</sdf>
"""

MODEL_CONFIG_TEMPLATE = """<?xml version="1.0"?>
<model>
  <name>{nome}</name>
  <version>1.0</version>
  <sdf version="1.8">model.sdf</sdf>
  <description>Quadro {indice} do ciclo de caminhada, extraido do esqueleto original.</description>
</model>
"""


def empacotar(dir_origem, nome_textura, nome_pessoa, n_frames):
    for i in range(n_frames):
        nome_modelo = f'{nome_pessoa}_frame_{i}'
        dir_destino = os.path.join(MODELS_DIR, nome_modelo)
        dir_meshes = os.path.join(dir_destino, 'meshes')
        os.makedirs(dir_meshes, exist_ok=True)

        shutil.copy(
            os.path.join(dir_origem, f'walk_{i:02d}.obj'),
            os.path.join(dir_meshes, 'walk.obj'))
        shutil.copy(
            os.path.join(dir_origem, f'walk_{i:02d}.mtl'),
            os.path.join(dir_meshes, 'walk.mtl'))
        if nome_textura and os.path.exists(nome_textura):
            shutil.copy(nome_textura, os.path.join(dir_meshes, os.path.basename(nome_textura)))

        # corrige mtllib/map_Kd pra nomes fixos (walk.mtl / nome real da textura)
        caminho_obj = os.path.join(dir_meshes, 'walk.obj')
        with open(caminho_obj) as f:
            conteudo = f.read()
        conteudo = conteudo.replace(f'walk_{i:02d}.mtl', 'walk.mtl')
        with open(caminho_obj, 'w') as f:
            f.write(conteudo)

        with open(os.path.join(dir_destino, 'model.sdf'), 'w') as f:
            f.write(MODEL_SDF_TEMPLATE.format(nome=nome_modelo))
        with open(os.path.join(dir_destino, 'model.config'), 'w') as f:
            f.write(MODEL_CONFIG_TEMPLATE.format(nome=nome_modelo, indice=i))

        print('empacotado:', nome_modelo)


if __name__ == '__main__':
    dir_origem, nome_textura, nome_pessoa, n_frames = (
        sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    empacotar(dir_origem, nome_textura, nome_pessoa, n_frames)
