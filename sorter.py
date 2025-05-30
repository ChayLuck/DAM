# disk_access_model/sorter.py
import os
import csv
import heapq
import tempfile

def get_file_size(filename):
    return os.path.getsize(filename)

def chunk_sort(input_file, memory_limit, sort_by):
    chunk_files = []
    with open(input_file, newline='') as infile:
        reader = csv.reader(infile)
        header = next(reader, None)
        chunk = []
        current_size = 0

        for row in reader:
            row_size = sum(len(x.encode()) for x in row)
            if current_size + row_size > memory_limit:
                chunk.sort(key=lambda x: float(x[sort_by]))
                temp = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
                writer = csv.writer(temp)
                if header:
                    writer.writerow(header)
                writer.writerows(chunk)
                temp.close()
                chunk_files.append(temp.name)
                chunk = []
                current_size = 0
            chunk.append(row)
            current_size += row_size

        if chunk:
            chunk.sort(key=lambda x: float(x[sort_by]))
            temp = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
            writer = csv.writer(temp)
            if header:
                writer.writerow(header)
            writer.writerows(chunk)
            temp.close()
            chunk_files.append(temp.name)

    return chunk_files

def merge_sorted_chunks(chunk_files, output_file, sort_by):
    min_heap = []
    files = [open(fname, newline='') for fname in chunk_files]
    readers = [csv.reader(f) for f in files]

    # Skip headers
    headers = next(readers[0])
    for r in readers[1:]:
        next(r, None)

    for i, reader in enumerate(readers):
        try:
            row = next(reader)
            heapq.heappush(min_heap, (float(row[sort_by]), i, row))
        except StopIteration:
            pass

    with open(output_file, 'w', newline='') as out:
        writer = csv.writer(out)
        writer.writerow(headers)
        while min_heap:
            _, i, row = heapq.heappop(min_heap)
            writer.writerow(row)
            try:
                next_row = next(readers[i])
                heapq.heappush(min_heap, (float(next_row[sort_by]), i, next_row))
            except StopIteration:
                pass

    for f in files:
        f.close()
    for fname in chunk_files:
        os.remove(fname)

def external_sort(input_file, output_file, memory_limit, sort_by):
    chunk_files = chunk_sort(input_file, memory_limit, sort_by)
    merge_sorted_chunks(chunk_files, output_file, sort_by)
