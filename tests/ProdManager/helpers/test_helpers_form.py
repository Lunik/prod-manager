import pytest

from ProdManager.helpers.form import (
  strip_input,
)

def test_strip_input():
  assert strip_input("") == ""
  assert strip_input("     tralala") == "tralala"
  assert strip_input("     tralala      ") == "tralala"
  assert strip_input("     tralala trilili    ") == "tralala trilili"
  assert strip_input("     tralala      trilili    ") == "tralala      trilili"
  assert strip_input("""
      tralala trilili    
  """) == "tralala trilili"
  assert strip_input("""
      tralala 
      trilili    

      trelele
  """) == "tralala\ntrilili\ntrelele"

  with pytest.raises(Exception):
    strip_input(dict())
