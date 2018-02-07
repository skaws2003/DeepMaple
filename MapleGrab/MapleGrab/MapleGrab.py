import FrontHandler_v2 as fh
import ParseArrow as pa
import ArrowTagger as at
import ArrowClassifier
import ArrowEdge
import glob

ARROW_PATH = ArrowClassifier.ARROW_PATH

if __name__ == '__main__':
    print("""
    Enter 'cap' to collect data
    Enter 'par' to parse arrows
    Enter 'dir' to tag arrow direction
    Enter 'cla' to classify arrow type
    Enter 'rec' to pack the data into .tfrecords
    """)
    command = input()
    
    if command == 'cap':
        print("\tLeft click to capture")
        print("\tRight click to undo capture")
        print("\tScroll click to adjust window position") 
        front = fh.Front(double=True)
        front.root.mainloop()
    elif command == 'par':
        parser = pa.Parser()
        parser.parse()
        parser.saveNumber()
    elif command == 'dir':
        ArrowTag = at.ArrowTagger()
        ArrowTag.root.mainloop()
    elif command == 'cla':
        print("""
        Left for full arrow
        Right for empty arrow
        """)
        ArrowClass = ArrowClassifier.ArrowClassifier()
        ArrowClass.root.mainloop()
    elif command == 'edg':
        print("Detecting edges...")
        AE = ArrowEdge.ArrowEdger()
        AE.Edge()
    else:
        print("Invalid command")
    
