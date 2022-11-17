from PIL.ImageTk import PhotoImage
import os


class GameImage:

    def __init__(self):
        """ Initializes a game image object that holds all the of the images for the game.
            The os library is used to get the current directory, and then iterates
            through all the images inside the 'images' directory. This makes all
            images available from different directories. """

        self.image_directory = r'..\assets\images'
        self.game_images = dict()

        for image in os.listdir(self.image_directory):
            self.game_images[image[:-4]] = PhotoImage(file=f'{self.image_directory}\\{image}')

    def return_image(self, image) -> PhotoImage:
        """ Returns the image from the image_directory given the image argument. """
        return self.game_images[image]
