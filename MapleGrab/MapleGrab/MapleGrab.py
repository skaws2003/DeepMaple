import FrontHandler_v2 as fh
import ParseArrow as pa
import ArrowTagger as at

print("""
Press 'c' to collect data
Press 'p' to parse arrows
Press 't' to tag data
Press 'r' to pack the data into .tfrecords
""")
command = input()

if command == 'c':
    print("\tLeft click to capture")
    print("\tRight click to undo capture")
    print("\tScroll click to adjust window position") 
    front = fh.Front()
    front.root.mainloop()
elif command == 'p':
    parser = pa.Parser()
    parser.parse()
    parser.saveNumber()
elif command == 't':
    ArrowTag = at.ArrowTagger()
    ArrowTag.root.mainloop()

