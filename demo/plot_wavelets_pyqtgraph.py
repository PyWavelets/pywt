import sys

import pywt
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg


families = ['db', 'sym', 'coif', 'bior', 'rbio']


def main():
    app = QtGui.QApplication(sys.argv)
    tabs = QtGui.QTabWidget()

    for family in families:
        scroller = QtGui.QScrollArea()
        vb = pg.GraphicsWindow()
        vb.setMinimumHeight(3000)
        vb.setMinimumWidth(1900)
        scroller.setWidget(vb)
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
            if i % 2 == 0:
                vb.nextRow()
        tabs.addTab(scroller, family)

    tabs.setWindowTitle('Wavelets')
    tabs.resize(1920, 1080)
    tabs.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
