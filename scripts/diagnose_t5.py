"""Is T5 separability all-zeros a real finding or a degenerate instrument?

Check: when we ablate Base-OS (=sensory+motor), do we trivially kill function by removing the
input/output themselves? A separability test must NOT ablate the sensory inputs or motor
outputs that the readout depends on -- otherwise every partition scores 0. Diagnose what each
ablation actually removes.
"""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tracks/T5-partition-separability/src"))

from shared.connectome import load_celegans, SENSORY, INTER, MOTOR
import ablate, partitions

c = load_celegans(path=ROOT / "data" / "celegans_real.npz")
model, bat = ablate.make_battery(c)
print(f"n={c.n}  sensory={int((c.roles==SENSORY).sum())} inter={int((c.roles==INTER).sum())} motor={int((c.roles==MOTOR).sum())}")
print(f"sensory_idx (inputs): {len(model.sensory_idx)}  motor_idx (readout): {len(model.motor_idx)}")

role_payload = partitions.role_based(c)          # True = interneurons
baseos = ~role_payload                            # sensory + motor
print(f"\nrole-based: payload(inter)={int(role_payload.sum())}  baseos(sens+motor)={int(baseos.sum())}")
# does ablating base-OS remove the motor readout neurons themselves?
motor_in_baseos = np.intersect1d(model.motor_idx, np.where(baseos)[0])
sens_in_baseos = np.intersect1d(model.sensory_idx, np.where(baseos)[0])
print(f"  motor readout neurons killed by base-OS ablation: {len(motor_in_baseos)}/{len(model.motor_idx)}")
print(f"  sensory input neurons killed by base-OS ablation:  {len(sens_in_baseos)}/{len(model.sensory_idx)}")
print("  -> if these are ~all, ablating base-OS trivially destroys I/O; separability undefined.")

# FPS when ablating ONLY interneurons (payload) -- inputs+outputs intact
f_payload = ablate.fps_after_lesion(c, model, bat, kill=role_payload)
f_baseos = ablate.fps_after_lesion(c, model, bat, kill=baseos)
print(f"\nFPS ablate payload(inter): {f_payload:.3f}   FPS ablate baseos(sens+motor): {f_baseos:.3f}")
