FourierInteractive

A number of test programs are included in a TestProgs/ directory that test individual features used in the final program. These can be used as stand-alone examples for use in other programs.

Test Programs
=============

TestFileDialog.py
  Test the tKinter file open dialog

TestOpenDisplayImage.py
  Use tKinter dialog to select image to display.
  Documented in WorkLog1

TestOpenDisplayImageAndChange.py
  Test interactive display using plt.pause(.001)
  plt.draw() is sometimes not enough for true interactive performance.

TestOpenDisplayAndFourier.py
  Opens image, displays it, then displays its Fourier transform
  using code from fft.py and its derivatives.
  Documented in WorkLog1

TestOpenDisplayAndFourierInverse.py
  Opens image, displays it, and its transform, does some simple filtering, then displays
  the inverse transform filtered image.

TestOpenDisplayAndFourInteractive.py
  Opens and displays image, Fourier transform, and inverse transform, then uses
  sliders to interactively set low-pass and high-pass filter thresholds. This program
  became the first version of FourierInteractive.py.

TestFourierDemo.py

TestOpenDisplayImageColormap.bak
  Failed attempt to adjust colormap interactively with a slider
  It works on a synthetic ramp image, but not an image read in from file using PIL.

TestOpenDisplayImageColormap.py

dynamic_image.py
  Example from on-line uses funcAnimation()

