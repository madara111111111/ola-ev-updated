# Prophet Installation Error on Windows

You are seeing:
```
ERROR: Could not install packages due to an OSError: [WinError 2] The system cannot find the file specified: 'C:\\Python312\\Scripts\\install_cmdstan.exe' -> 'C:\\Python312\\Scripts\\install_cmdstan.exe.deleteme'
```

## Why?

- Prophet (and its dependency `cmdstanpy`) needs to install CmdStan, which requires a C++ toolchain and sometimes fails on Windows due to missing build tools or permissions.

## How to fix

1. **Run your terminal as Administrator** (right-click → Run as Administrator).
2. **Install Visual C++ Build Tools**  
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install the "Desktop development with C++" workload.
3. **Try installing Prophet again:**
   ```
   pip install prophet
   ```
4. **If you still get errors, try installing with conda (recommended for Prophet):**
   ```
   conda install -c conda-forge prophet
   ```
   (You need Anaconda or Miniconda for this.)

5. **If you only need to run, not train, the model:**  
   - You can train Prophet on Linux and copy the saved model to Windows, but for most use cases, Prophet needs to be installed on the machine where you run predictions.

## How to save and load a Prophet model

Prophet models can be saved using Python's `pickle` module:

```python
import pickle

# To save a trained Prophet model
with open('prophet_model.pkl', 'wb') as f:
    pickle.dump(prophet_model, f)

# To load a saved Prophet model
with open('prophet_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
```

- Make sure to use the same Prophet version for saving and loading.
- The `.pkl` file can be moved between machines with compatible Python/Prophet versions.

## Alternative

- Use a Linux environment (e.g., WSL, Ubuntu VM, or cloud) for Prophet development and training.

---

**Summary:**  
- Prophet is tricky to install on Windows due to C++ dependencies.
- Use conda or install build tools, or switch to Linux for Prophet work.
