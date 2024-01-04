class Utils:
  def zero_pad(self, input, handle_minus = False):
    if isinstance(input, str):
      mod = ' greater than ' if ('+') in input else ''
      input = input.replace('+', '')

      return '{}{}'.format(mod, input).strip()

    minus = ' minus ' if handle_minus and input < 0 else ''
    zero_pad = '0' if input < 10 else ''

    return '{}{}{}'.format(minus, zero_pad, input).strip()
