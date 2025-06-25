import sys
from fpdf import FPDF

class Shirtificate(FPDF):
    def __init__(self, name, custom_title="CS50 Shirtificate", new_color = "White", url_image="shirtificate.png", output_file="shirtificate.pdf"):
        super().__init__()
        self.name = name
        self.custom_title = custom_title
        self.new_color = new_color
        self.UrlImage = url_image
        self.output_file = output_file

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, output_file):
        if not isinstance(output_file, str) or not output_file.strip():
            self._output_file = "shirtificate.pdf"
        else:
            self._output_file = output_file.strip()

    @property
    def UrlImage(self):
        return self._UrlImage

    @UrlImage.setter
    def UrlImage(self, url_image):
        if not isinstance(url_image, str) or not url_image.strip():
            raise ValueError("Image URL must be a non-empty string")
        self._UrlImage = url_image.strip()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = new_name.strip()

    @property
    def custom_title(self):
        return self._custom_title

    @custom_title.setter
    def custom_title(self, new_title):
      if not isinstance(new_title, str) or not new_title.strip():
          self._custom_title = "CS50 Shirtificate"  # valeur par défaut
      else:
          self._custom_title = new_title.strip()

    @property
    def new_color(self):
        return self._new_color

    @new_color.setter
    def new_color(self, new_color):
      new_color = new_color.strip().lower()
      match new_color:
          case "white":
              new_color = [255, 255, 255]
          case "black":
              new_color = [0, 0, 0]
          case "red":
              new_color = [255, 0, 0]
          case "green":
              new_color = [0, 255, 0]
          case "blue":
              new_color = [0, 0, 255]
          case _:
              raise ValueError("Color must be one of the predefined colors: White, Black, Red, Green, Blue")

      self._new_color = new_color

    def generate_pdf(self):
        self.add_page()

        # Set font for the title
        self.ln(20)
        self.set_font(family="helvetica", size=50)
        title_width = self.get_string_width(self.custom_title) + 6
        x = (self.w - title_width) / 2
        self.set_x(x)
        self.cell(title_width, 15, self.custom_title, align="C")

        # Set Image
        self.ln(40)
        image_width = 200
        image_x = (self.w - image_width) / 2
        image_y = self.get_y()
        self.image(self.UrlImage, x=image_x, y=image_y, w=image_width)

        # Message in shirtificate Image
        self.ln(70)
        self.set_font(family="helvetica", size=30)
        self.set_text_color(*self.new_color)
        message = f"{self.name} took CS50"
        message_width = self.get_string_width(message) + 6
        x = (self.w - message_width) / 2
        self.set_x(x)
        self.cell(message_width, 15, message, align="C")

        self.output(self.output_file)

def main():
      title = "CS50 Shirtificate"
      name = input("Name: ")
      color = "White"
      p = Shirtificate(name, title, color)
      p.generate_pdf()

main()
