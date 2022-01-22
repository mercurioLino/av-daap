# import numpy as np
# from sklearn.base import BaseEstimator, TransformerMixin
# from skimage.feature import hog
# from skimage.io import imread
# from skimage.transform import rescale
# import skimage 

# class RGB2GrayTransformer(BaseEstimator, TransformerMixin):
#     def __init__(self):
#         pass
 
#     def fit(self, X, y=None):
#         return self
 
#     def transform(self, X, y=None):
#         return np.array([skimage.color.rgb2gray(img) for img in X])
     
# class HogTransformer(BaseEstimator, TransformerMixin):
#     def __init__(self, y=None, orientations=9,
#                  pixels_per_cell=(8, 8),
#                  cells_per_block=(3, 3), block_norm='L2-Hys'):
#         self.y = y
#         self.orientations = orientations
#         self.pixels_per_cell = pixels_per_cell
#         self.cells_per_block = cells_per_block
#         self.block_norm = block_norm
 
#     def fit(self, X, y=None):
#         return self
 
#     def transform(self, X, y=None):
 
#         def local_hog(X):
#             return hog(X,
#                        orientations=self.orientations,
#                        pixels_per_cell=self.pixels_per_cell,
#                        cells_per_block=self.cells_per_block,
#                        block_norm=self.block_norm)
 
#         try:
#             return np.array([local_hog(img) for img in X])
#         except:
#             return np.array([local_hog(img) for img in X])