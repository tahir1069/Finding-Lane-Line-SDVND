#%%
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import imageio
import Lane_Lines_Finding as LLF
#%matplotlib inline
#%%
test_pics = os.listdir("test_images/")
test_vids = os.listdir("test_videos/")
#%%
for i in test_pics:
    i = 'test_images/' + i
    if i == 'test_images/Thumbs.db':
        pass
    else:        
        j = 'output_' + i + '.jpeg'
        image = mpimg.imread(i)
        final = LLF.lane_lines(img = image)
        #final = prog.lane_lines(image)
        plt.imshow(final)  #call as plt.imshow(gray, cmap='gray') to show a grayscaled img
        mpimg.imsave(j, final)
        plt.show()
#%%
for i in test_vids:
    i = 'test_videos/' + i
    j = 'output_test_videos/' + i + '.mp4'
    if i == 'test_videos/Thumbs.db':
        pass      
    elif i == 'test_videos/challenge.mp4':
        pass
    else:        
        j = 'output_' + i
        print(i)
        print(j)
        reader = imageio.get_reader(i) 
        fps = reader.get_meta_data()['fps'] # We get the fps frequence (frames per second).
        writer = imageio.get_writer(j, fps = fps) # We create an output video with this same fps frequence.
        for K, frame in enumerate(reader): # We iterate on the frames of the output video:
            final = LLF.lane_lines(img = frame)
            writer.append_data(final) # We add the next frame in the output video.
            print(K) # We print the number of the processed frame.
        writer.close() # We close the process that handles the creation of the output video.
#%%