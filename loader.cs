using UnityEngine;
using System.Collections;
using System.Net;
using System;

public class Loader : MonoBehaviour
{

    private int count = 0;
    private int prev_frame = 0;
    private Renderer r;
    private WWW imglink;
    public string image_folder;
    public int frame_gap = 4;

    // Use this for initialization
    void Start()
    {

    }

    void Update()
    {
        count++;
        if (count % frame_gap == 0)
        {
            StartCoroutine(LoadImg());
        }
    }

    IEnumerator LoadImg()
    {
        WebClient web = new WebClient();
        System.IO.Stream stream = web.OpenRead(string.Format("http://vac5:80/{0}/store.txt", image_folder));
        using (System.IO.StreamReader reader = new System.IO.StreamReader(stream))
        {
            string s;
            try
            {
                String text = reader.ReadToEnd();
                int x = 1 * Convert.ToInt32(text);
                s = string.Format("http://vac5:80/{0}/{1}.jpg", image_folder, x);
                prev_frame = x;
            }
            catch
            {
                s = string.Format("http://vac5:80/{0}/{1}.jpg", image_folder, prev_frame);
            }
            imglink = new WWW(s);
            yield return imglink;
            r = GetComponent<Renderer>();
            Destroy(r.material.mainTexture);
            r.material.mainTexture = imglink.texture;
        }
    }
}
