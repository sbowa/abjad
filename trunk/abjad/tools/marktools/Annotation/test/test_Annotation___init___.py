from abjad import *


def test_Annotation___init____01( ):
   '''Initialize annotation with dictionary.
   '''

   dictionary = { }
   annotation = marktools.Annotation(dictionary)
   assert annotation.contents == dictionary
   assert annotation.contents is not dictionary
   

