Attribute VB_Name = "Module1"
Sub ImportCSVtoBetsSheetAndSort()
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Bets")
    
    Dim csvFile As String
    csvFile = Application.GetOpenFilename("CSV Files (*.csv), *.csv", , "Select CSV File")
    If csvFile = "False" Then Exit Sub
    
    Dim csvContent As String
    Dim fileNum As Integer
    fileNum = FreeFile
    
    Open csvFile For Input As #fileNum
    csvContent = Input$(LOF(fileNum), fileNum)
    Close #fileNum
    
    Dim csvLines() As String
    csvLines = Split(csvContent, vbCrLf)
    
    Dim csvHeaders() As String
    csvHeaders = Split(csvLines(0), ",")
    
    Dim headerMap As Object
    Set headerMap = CreateObject("Scripting.Dictionary")
    
    Dim i As Integer, j As Integer
    For i = LBound(csvHeaders) To UBound(csvHeaders)
        csvHeaders(i) = Trim(csvHeaders(i))
        For j = 1 To 25 ' Columns A to Y (25 columns)
            If ws.Cells(9, j).Value = csvHeaders(i) Then
                headerMap.Add csvHeaders(i), j
                Exit For
            End If
        Next j
    Next i
    
    Dim nextRow As Long
    nextRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row + 1
    If nextRow < 11 Then nextRow = 11
    
    Dim line As String, lineData() As String
    Dim notesCol As Long
    notesCol = headerMap("Notes")
    
    For i = 1 To UBound(csvLines)
        line = csvLines(i)
        If Trim(line) <> "" Then
            lineData = Split(line, ",")
            Dim foundRow As Long
            foundRow = 0
            ' Search for existing entry in Notes column
            For j = 11 To ws.Cells(ws.Rows.Count, notesCol).End(xlUp).Row
                If ws.Cells(j, notesCol).Value = lineData(1) Then           ' Notes is the second column in the csv file
                    foundRow = j
                    Exit For
                End If
            Next j
            
            If foundRow = 0 Then foundRow = nextRow
            
            ' Insert/Update row data
            For j = LBound(lineData) To UBound(lineData)
                If headerMap.exists(csvHeaders(j)) Then
                    ws.Cells(foundRow, headerMap(csvHeaders(j))).Value = lineData(j)
                End If
            Next j
            
            If foundRow = nextRow Then nextRow = nextRow + 1
        End If
    Next i
    
    ' Sort by Date Column (Column A)
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    If lastRow > 11 Then
        With ws.Sort
            .SortFields.Clear
            .SortFields.Add Key:=ws.Range("A11:A" & lastRow), _
                            SortOn:=xlSortOnValues, _
                            Order:=xlAscending, _
                            DataOption:=xlSortNormal
            .SetRange ws.Range("A11:Y" & lastRow)
            .Header = xlYes
            .MatchCase = False
            .Orientation = xlTopToBottom
            .SortMethod = xlPinYin
            .Apply
        End With
    End If
    
    MsgBox "CSV data successfully imported into the 'Bets' sheet and sorted by date.", vbInformation
End Sub


