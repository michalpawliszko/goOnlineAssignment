class Color:
    """This class is used to calculate and hold color object informations like, rgba, hex, hsl.
    Objects can be created based on hex or rgba values format."""

    def __init__(self, hex=None, rgba=None):
  
        if hex==None and rgba==None:
            raise ValueError("Must enter either a hex or rgb value")

        elif hex != None and rgba != None:
            raise ValueError("Can't input rgb and hex at the same time")

        elif hex != None:
            self.hex = hex
            self.rgba = self.hex_to_rgb(hex)

        elif rgba != None:
            self.rgba = rgba
            self.hex = self.rgba_to_hex(rgba)

        self.hsl = self.rgba_to_hsl(self.rgba)

    def hex_to_rgb(self, hex_nr: str):
        """ Convert hex format to rgba format"""

        hex_nr = hex_nr.replace("#", "")

        return tuple(int(hex_nr[i:i+2],16) for i in range(0,len(hex_nr),2))

    def rgba_to_hex(self,rgba_nr: tuple):
        """ Convert rgba format to hex format """

        return "#"+"%02x%02x%02x%02x" % rgba_nr


    def rgba_to_hsl(self,rgba_nr: tuple):
        """Calculates hue, saturation, lightness based on rgba"""

        r,g,b = (n/255 for n in rgba_nr[:3])

        min_value = min((r,g,b))
        max_value = max((r,g,b))

        lightness = (min_value + max_value)/2

        if r==g and g==b and b==r:
            hue=0
            saturation =0.0
        
        else:

            if lightness <=0.5:

                saturation = (max_value-min_value)/(max_value+min_value)
            elif lightness > 0.5:
                saturation = (max_value-min_value)/(2.0 -max_value-min_value)
            
            max_idx = (r,g,b).index(max_value)

            if max_idx == 0:
                hue = ((g-b)/(max_value-min_value)) * 60
                if hue < 0:
                    hue = 360+hue
            elif max_idx == 1:
                hue = (2.0+(b-r)/(max_value-min_value)) * 60
                if hue < 0:
                    hue = 360+hue
            elif max_idx == 2:
                hue = (4.0 + (r-g)/(max_value-min_value)) * 60
                if hue < 0:
                    hue = 360+hue

        return round(hue), saturation, lightness


    def change_saturation(self, new_saturation):

        """ Calculates and updates new rgba and hex values of color obcject based on new saturation"""

        alpha = self.rgba[-1]
        h = round(self.hsl[0],3)
        l=round(self.hsl[-1],3)
        new_saturation = round(new_saturation,3)

        if h == 0:

            new_r = new_g= new_b= round(l*255)

        else:

            if l<0.5:
                tmp1 = l*(1.0+new_saturation)
            elif l>=0.5:
                tmp1 = l + new_saturation - l*new_saturation

            tmp2 = 2*l - tmp1

            converted_hue = h/360

            tmp_r = converted_hue + 0.333
            if tmp_r>1:
                tmp_r= tmp_r -1
            
            tmp_g = converted_hue

            tmp_b = converted_hue - 0.333
            if tmp_b<0:
                tmp_b = tmp_b+1

            #calculate new r
            if 6*tmp_r<1:
                new_r = round((tmp2+(tmp1-tmp2) * 6 * tmp_r) * 255)
            
            elif 2*tmp_r<1:
                new_r = round(tmp1 * 255)

            elif 3*tmp_r<2:
                new_r = round((tmp2 + (tmp1-tmp2) * (0.666-tmp_r) * 6) * 255)

            else:
                new_r = round(tmp2 * 255)


            # calculate new g
            if 6*tmp_g<1:
                new_g = round((tmp2+(tmp1-tmp2) * 6 * tmp_g) * 255)
            
            elif 2*tmp_g<1:
                new_g = round(tmp1 * 255)

            elif 3*tmp_g<2:
                new_g = round((tmp2 + (tmp1-tmp2) * (0.666-tmp_g) * 6) * 255)

            else:
                new_g = round(tmp2 * 255)

            # calculate new_b
            if 6*tmp_b<1:
                new_b = round((tmp2+(tmp1-tmp2) * 6 * tmp_b) * 255)
            
            elif 2*tmp_b<1:
                new_b = round(tmp1 * 255)

            elif 3*tmp_b<2:
                new_b = round((tmp2 + (tmp1-tmp2) * (0.666-tmp_b) * 6) * 255)

            else:
                new_b = round(tmp2 * 255)


        self.rgba = (new_r,new_g, new_b, alpha)

        self.hsl = (h,new_saturation,l)

        self.hex = self.rgba_to_hex((new_r,new_g, new_b, alpha))


    def show_details(self):

        print(f""" 
        red:\t{self.rgba[0]}
        green:\t{self.rgba[1]}
        blue:\t{self.rgba[2]}
        alpha:\t{self.rgba[3]}
        hex:\t{self.hex}
        hue:\t{self.hsl[0]}
        saturation:\t{self.hsl[1]:.3f}
        lightness:\t{self.hsl[2]:.3f}
        """)

