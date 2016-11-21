import sys

from PyQt4 import QtGui

import pywt
import pyqtgraph as pg


families = ['db', 'sym', 'coif', 'bior', 'rbio']


def main():
    app = QtGui.QApplication(sys.argv)
    tabs = QtGui.QTabWidget()

    for family in families:
        vb = pg.GraphicsWindow()
        for i, name in enumerate(pywt.wavelist(family)):
            pen = pg.intColor(i)
            wavelet = pywt.Wavelet(name)
            if wavelet.orthogonal:
                phi, psi, x = wavelet.wavefun(level=5)
                ax = vb.addPlot(title=wavelet.name + " phi")
                ax.plot(phi, pen=pen)
                bx = vb.addPlot(title=wavelet.name + " psi")
                bx.plot(psi, pen=pen)
            else:
                phi, psi, phi_r, psi_r, x = wavelet.wavefun(level=5)
                ax = vb.addPlot(title=wavelet.name + " phi")
                ax.plot(phi, pen=pen)
                bx = vb.addPlot(title=wavelet.name + " psi")
                bx.plot(psi, pen=pen)
                ax = vb.addPlot(title=wavelet.name + " phi_r")
                ax.plot(phi_r, pen=pen)
                bx = vb.addPlot(title=wavelet.name + " psi_r")
                bx.plot(psi_r, pen=pen)
            if ((not wavelet.orthogonal) and i % 2 == 0) or i % 4 == 0:
                vb.nextRow()
        tabs.addTab(vb, family)

    tabs.resize(1200, 800)

    tabs.setWindowTitle('Wavelets')
    tabs.showMaximized()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
