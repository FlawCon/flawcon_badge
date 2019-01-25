QR Code Library Reference
=========================

.. py:module:: qr

.. py:attribute:: ECC_LOW

    The lowest possible error correction

.. py:attribute:: ECC_MEDIUM

    Medium error correction

.. py:attribute:: ECC_QUARTILE

    Quartile error correction

.. py:attribute:: ECC_HIGH

    The higher possible error correction

.. py:class:: QR(version, ecc)

    A class to generate QR code data. Note this class does not generate the pixel data, but merely the value of each module.
    See the :py:meth:`matrix` method documentation for more information.

    :param version: The version of QR code to use, 1-40 inclusive. The higher the version the more data that can be stored.
    :param ecc: The level of error correction to apply, set using the ECC_* constants above

    .. py:method:: write(data)

        Writes data to the buffer of the QR code creator

        :param data: The data to write to the QR code's buffer

    .. py:method:: matrix()

        Generates and returns a square 2D array of the value of each 'module' in the QR code. Each module is not necessarily a single pixel
        (in fact that'd be tiny). ``True`` correlates with white and ``False`` with black. A 1 module wide white border
        is included in the output but this is the bare minimum to scan, and more is advised.

        **Note:** after calling matrix calling :py:meth:`write` will be a noop and calling this function again will return
        the exact same data
