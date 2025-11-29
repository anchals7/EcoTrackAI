# Prophet Setup Guide for Windows

Prophet requires `cmdstanpy` (the Stan backend) to work on Windows. Here's how to set it up:

## Quick Setup

```powershell
# In your venv
python -m pip install cmdstanpy

# Install CmdStan (this downloads ~100MB)
python -m cmdstanpy.install_cmdstan
```

## Detailed Steps

### 1. Install cmdstanpy
```powershell
python -m pip install cmdstanpy
```

### 2. Install CmdStan
This downloads and installs the CmdStan compiler (required for Prophet):
```powershell
python -m cmdstanpy.install_cmdstan
```

This will:
- Download CmdStan (~100MB)
- Compile it (takes a few minutes)
- Set it up in your user directory

### 3. Verify Installation
```powershell
python -c "import cmdstanpy; print('CmdStan path:', cmdstanpy.cmdstan_path())"
```

If this prints a path, you're good!

### 4. Test Prophet
```powershell
python -c "from prophet import Prophet; print('✅ Prophet works!')"
```

## Troubleshooting

### "CmdStan installation failed"
- Make sure you have C++ build tools installed
- On Windows, you may need Visual Studio Build Tools
- Try: `python -m cmdstanpy.install_cmdstan --compiler` to use a different compiler

### "Still getting stan_backend error"
- Restart your Python environment
- Make sure you're in the venv
- Try: `python -c "import cmdstanpy; cmdstanpy.install_cmdstan(version='latest')"`

### Alternative: Use Simple Forecast
If Prophet is too complex to set up, the simple forecast fallback works fine for MVP/demo purposes. It uses your recent average emissions to project forward.

## For MVP/Demo

**You don't need Prophet!** The simple forecast fallback is sufficient and demonstrates the forecasting feature. Prophet is nice-to-have for more sophisticated predictions, but not required.

