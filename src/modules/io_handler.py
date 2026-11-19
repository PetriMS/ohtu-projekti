import pathlib


class IOHandler:
    """
    IO-käsittelijä.
    """

    def console_read_input(self, text: str):
        """
        Lukee syötteen konsolista kuten `input()`
        """
        return input(text)

    def console_print(self, text: str):
        """
        Kirjoittaa konsoliin kuten `print()`
        """
        print(text)

    def read_file(self, file_path: str):
        """
        Avaa tiedoston ja lukee ja palauttaa sen sisällön
        """
        path = pathlib.Path(file_path)

        contents = ""
        with path.open(mode="r") as f:
            contents = f.read()

        return contents

    def write_file(self, data: str, file_path: str):
        """
        Avaa tiedoston ja kirjoittaa annetun datan sinne
        """
        path = pathlib.Path(file_path)

        with path.open(mode="w") as f:
            f.write(data)
